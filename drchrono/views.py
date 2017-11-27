import datetime
import re

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required

from .forms import PatientCheckinForm, DemographicsForm
from .models import Appointment
from . import drchrono_api
from .utils import conv_time


@login_required()
def appt(request):
    """starting screen for appointment checkins (patient-facing)"""
    access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]
    data = drchrono_api.get_todays_appointments(access_token)

    appts = [
        {'id': i['id'], 'patient': i['patient'], 'time':conv_time(i['scheduled_time'][-8:-3])}
        for i
        in data['results']
        if i['status'] == '']
    return render(request, 'appointments.html', {'appts': appts})


@login_required()
def patient_checkin(request, appt_id, patient_id):
    """confirms patient's identity with information saved on drcrhono's API"""

    if request.method == 'POST':
        form = PatientCheckinForm(request.POST)
        if form.is_valid():
            # look up the user
            access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]
            data = drchrono_api.get_patient(access_token, patient_id)

            if data is None:
                raise Http404("Patient not found.")

            print(data['first_name'])
            print(data['last_name'])
            print(data['social_security_number'])

            fields = ('first_name', 'last_name')
            for i in fields:
                if len(data[i]) > 0 and form.cleaned_data[i].lower() != data[i].lower():
                    form.add_error(i, 'Patient info on file does not match.')

            # further sanitize ssn
            data_ssn = re.sub(r"(?!\d).?", "", data['social_security_number'])
            form_ssn = re.sub(r"(?!\d).?", "", form.cleaned_data['social_security_number'])
            if len(data['social_security_number']) > 0 and data_ssn != form_ssn:
                form.add_error('social_security_number', 'Patient info on file does not match.')

            if len(form.errors) == 0:
                return HttpResponseRedirect(reverse('demog', args=[appt_id, patient_id]))
    else:
        form = PatientCheckinForm()

    return render(
        request,
        'patient_login.html',
        {'form': form})


@login_required()
def demographics(request, appt_id, patient_id):
    """Handles updating demographics information"""
    access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]

    if request.method == 'POST':
        form = DemographicsForm(request.POST)
        if form.is_valid():
            # update patient demographic info
            response = drchrono_api.put_patient(access_token, patient_id, form.cleaned_data)

            # handle API response
            if 200 <= response.status_code < 400:
                return HttpResponseRedirect(reverse('checkin', args=[appt_id]))
            else:
                form.add_error(None, 'Data not submitted. Please try again.')
    else:
        # query API for patient data, then populate form
        data = drchrono_api.get_patient(access_token, patient_id)

        form = DemographicsForm(initial=data)

    return render(
        request,
        'demographic.html',
        {
            'form': form,
            'appt_id': appt_id,
            'patient_id': patient_id})


# TODO: add appointment details verification screen?


@login_required()
def check_in(request, appt_id):
    """sets appointment status to arrived

    sets arrival time for appointment in database
    """
    access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]
    appointment_data = drchrono_api.get_appointment(access_token, appt_id)

    if appointment_data is None:
        raise Http404("Appointment not found.")

    # scrape required fields only (don't want to modify other things)
    appointment = {
        'doctor': appointment_data['doctor'],
        'duration': appointment_data['duration'],
        'exam_room': appointment_data['exam_room'],
        'office': appointment_data['office'],
        'patient': appointment_data['patient'],
        'scheduled_time': appointment_data['scheduled_time'],
        'status': 'Arrived'
    }
    response = drchrono_api.put_appointment(access_token, appt_id, appointment)

    # handle API response
    if 200 <= response.status_code < 400:
        # create entry in database
        appt = Appointment.objects.create(appointment_id=appt_id)
        appt.save()
    else:
        # somehow denote error; redirect to error screen? only
        # option is to return to the main menu?
        print(response.status_code)
        pass
        # form.add_error(None, 'Data not submitted. Please try again.')

    # TODO: show brief appointment details?

    return render(
        request,
        'checkin.html')


@login_required()
def waitlist(request):
    """Handles the doctor-facing waitlist

    * calculates average wait time
    * lists currently waiting patients
    * allows doctors to mark patients as "seen"
    """

    if request.method == 'POST':
        # TODO create form and clean input data
        print(request.POST['id'])
        appt = Appointment.objects.get(id=request.POST['id'])
        appt.seen = datetime.datetime.utcnow().replace(tzinfo=utc)
        appt.save()

        # Should this be changing anything on the API?

        return HttpResponseRedirect(reverse('d_waitlist'))
    else:
        appointments = []
        for appt in Appointment.objects.exclude(seen__isnull=False):
            # This is not great (2 dependent API calls per appointment?!), but will work for now

            # get appointment data
            access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]

            appointment_data = drchrono_api.get_appointment(access_token, appt.appointment_id)
            print(appointment_data)
            patient_data = drchrono_api.get_patient(access_token, appointment_data['patient'])
            print(patient_data)

            appointments.append({
                'id': appt.id,
                'scheduled_time': conv_time(appointment_data['scheduled_time'][-8:-3]),
                'elapsed_time': int((datetime.datetime.utcnow().replace(tzinfo=utc) - appt.check_in).total_seconds() / 60),
                'patient_name': "{} {}".format(patient_data['first_name'], patient_data['last_name']),
            })

        # calculate average wait time
        wait_times = []
        for appt in Appointment.objects.all():
            seen_time = appt.seen if appt.seen is not None else datetime.datetime.utcnow().replace(tzinfo=utc)
            wait_times.append((seen_time - appt.check_in).total_seconds() / 60)
        avg_wait_time = int(sum(wait_times)/len(wait_times)) if len(wait_times) > 0 else 0

    # TODO make template prettier (ailghn left?)
    return render(
        request,
        'd_waitlist.html',
        {
            'appointments': appointments,
            'avg_wait_time': avg_wait_time,
        })


def home(request):
    """Login if not logged in already, otherwise redirect to device choice screen"""
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse('begin'))
    return render(request, "index.html")


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))

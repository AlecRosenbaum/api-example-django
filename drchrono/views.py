import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required

import requests

from .forms import PatientCheckinForm, DemographicsForm
from .settings import DRCHRONO_API_BASE
from .models import Appointment


@login_required()
def appt(request):
    """starting screen for appointment checkins (patient-facing)"""
    access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]
    response = requests.get(
        DRCHRONO_API_BASE + 'appointments',
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
        }, params={
            'date': str(datetime.date.today()),
        })
    data = response.json()
    # TODO move all api calls into drchrono_api.py

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
            response = requests.get(
                DRCHRONO_API_BASE + 'patients/{}'.format(patient_id),
                headers={
                    'Authorization': 'Bearer {}'.format(access_token),
                })
            data = response.json()
            print(data)
            print(data['first_name'])
            print(data['last_name'])
            print(data['social_security_number'])

            # TODO verify data was actually returned, remove print

            fields = ('first_name', 'last_name', 'social_security_number')
            for i in fields:
                if len(data[i]) > 0 and form.cleaned_data[i].lower() != data[i].lower():
                    form.add_error(i, 'Patient info on file does not match.')

            # TODO handle ssn properly/ do comparison without spaces/dashes/etc

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
            # process the data in form.cleaned_data as required
            response = requests.put(
                DRCHRONO_API_BASE + 'patients/{}'.format(patient_id),
                headers={
                    'Authorization': 'Bearer {}'.format(access_token),
                },
                data=form.cleaned_data)

            # handle API response
            if 200 <= response.status_code < 400:
                return HttpResponseRedirect(reverse('checkin', args=[appt_id]))
            else:
                form.add_error(None, 'Data not submitted. Please try again.')

    else:
        # query API for patient data, then populate form
        response = requests.get(
            DRCHRONO_API_BASE + 'patients/{}'.format(patient_id),
            headers={
                'Authorization': 'Bearer {}'.format(access_token),
            })
        data = response.json()

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
    response = requests.get(
        DRCHRONO_API_BASE + 'appointments/{}'.format(appt_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
        })
    apppointment_data = response.json()

    # TODO check that data is really there

    # scrape required fields only (don't want to modify other things)
    appointment = {
        'doctor': apppointment_data['doctor'],
        'duration': apppointment_data['duration'],
        'exam_room': apppointment_data['exam_room'],
        'office': apppointment_data['office'],
        'patient': apppointment_data['patient'],
        'scheduled_time': apppointment_data['scheduled_time'],
        'status': 'Arrived'
    }
    response = requests.put(
        DRCHRONO_API_BASE + 'appointments/{}'.format(appt_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
        },
        data=appointment)

    # TODO verify put was successful

    # create entry in database
    appt = Appointment.objects.create(appointment_id=appt_id)
    appt.save()

    # TODO: show breif appointment details?

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
            response = requests.get(
                DRCHRONO_API_BASE + 'appointments/{}'.format(appt.appointment_id),
                headers={
                    'Authorization': 'Bearer {}'.format(access_token),
                })
            appointment_data = response.json()

            # get patient data
            response = requests.get(
                DRCHRONO_API_BASE + 'patients/{}'.format(appointment_data['patient']),
                headers={
                    'Authorization': 'Bearer {}'.format(access_token),
                })
            patient_data = response.json()

            appointments.append({
                'id': appt.id,
                'scheduled_time': conv_time(appointment_data['scheduled_time'][-8:-3]),
                'elapsed_time': int((datetime.datetime.utcnow().replace(tzinfo=utc) - appt.check_in).total_seconds() / 60),  # TODO actually calculate using check_in time and now
                'patient_name': "{} {}".format(patient_data['first_name'], patient_data['last_name']),
            })

        # calculate average wait time
        wait_times = []
        for appt in Appointment.objects.all():
            seen_time = appt.seen if appt.seen is not None else datetime.datetime.utcnow().replace(tzinfo=utc)
            wait_times.append((seen_time - appt.check_in).total_seconds() / 60)
        avg_wait_time = int(sum(wait_times)/len(wait_times)) if len(wait_times) > 0 else 0

    # TODO make template prettier (ailght left?)
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


# TODO move and formalize this, this is not a view, just a utility function
def conv_time(time_str):
    """converts HH:MM -> H:MM PM"""
    hr = int(time_str[:2])
    mn = int(time_str[4:])
    suffix = "PM" if hr >= 12 else "AM"
    if hr > 12:
        hr = hr % 12
    return "{}:{:02d} {}".format(hr, mn, suffix)

import datetime
import re

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator

from .forms import PatientCheckinForm, DemographicsForm, DoctorWaitlistForm
from .models import Appointment
from . import drchrono_api
from .utils import conv_time


class Appt(View):
    def get(self, request):
        """starting screen for appointment checkins (patient-facing)"""
        access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]
        data = drchrono_api.get_todays_appointments(access_token)

        appts = [
            {'id': i['id'], 'patient': i['patient'], 'time':conv_time(i['scheduled_time'][-8:-3])}
            for i
            in data['results']
            if i['status'] == '']
        return render(request, 'appointments.html', {'appts': appts})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)


class PatientCheckin(View):
    """confirms patient's identity with information saved on drcrhono's API"""
    form_class = PatientCheckinForm
    template = 'patient_login.html'

    def get(self, request, appt_id, patient_id):
        """render form"""
        form = self.form_class()

        return render(
            request,
            self.template,
            {'form': form})

    def post(self, request, appt_id, patient_id):
        """validate info, redirect if successful"""
        form = self.form_class(request.POST)
        if form.is_valid():
            # look up the user
            access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]
            data = drchrono_api.get_patient(access_token, patient_id)

            if data is None:
                raise Http404("Patient not found.")

            # TODO remove - this makes testing a lot easier
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
        return render(
            request,
            self.template,
            {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)


class Demographics(View):
    """handles updating demographics information"""
    form_class = DemographicsForm
    template = 'demographic.html'

    def get(self, request, appt_id, patient_id):
        access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]

        # query API for patient data, then populate form
        data = drchrono_api.get_patient(access_token, patient_id)

        # replace stray characters in phone numbers
        phone_fields = (
            'home_phone',
            'cell_phone',
            'office_phone',
            'emergency_contact_phone',
            'responsible_party_phone',)
        for i in phone_fields:
            data[i] = re.sub(r"(?!\d).?", "", data[i])
        form = self.form_class(initial=data)

        return render(
            request,
            self.template,
            {
                'form': form,
                'appt_id': appt_id,
                'patient_id': patient_id,
                'patient_photo': data['patient_photo'],
            })

    def post(self, request, appt_id, patient_id):
        access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]

        # query API for patient data, then populate form
        data = drchrono_api.get_patient(access_token, patient_id)

        form = self.form_class(request.POST)
        if form.is_valid():
            # update patient demographic info
            response = drchrono_api.put_patient(access_token, patient_id, form.cleaned_data)

            # handle API response
            if 204 == response.status_code:
                return HttpResponseRedirect(reverse('checkin', args=[appt_id]))
            else:
                print(response)
                print(response.status_code)
                print(response.json())
                form.add_error(None, 'Data not submitted. Please try again.')

        return render(
            request,
            self.template,
            {
                'form': form,
                'appt_id': appt_id,
                'patient_id': patient_id,
                'patient_photo': data['patient_photo'],
            })

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)


# TODO: add appointment details verification screen?


class Checkin(View):
    """sets appointment status to arrived

    sets arrival time for appointment in database
    """
    def get(self, request, appt_id):
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
            # Show error screen
            return render(request, 'checkin_error.html')

        return render(
            request,
            'checkin.html',
            {
                'appointment': {
                    'reason': appointment_data['reason'],
                    'scheduled_time': conv_time(appointment_data['scheduled_time'][-8:-3]),
                    'duration': appointment_data['duration'],
                }
            })

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)


class Waitlist(View):
    """Handles the doctor-facing waitlist

    * calculates average wait time
    * lists currently waiting patients
    * allows doctors to mark patients as "seen"
    """
    template = 'd_waitlist.html'

    def get(self, request):
        appointments = []
        for appt in Appointment.objects.exclude(seen__isnull=False):
            # This is not great (2 dependent API calls per appointment?!), but will work for now

            # get appointment data
            access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]

            appointment_data = drchrono_api.get_appointment(access_token, appt.appointment_id)
            if appointment_data is None:
                raise Http404("Appointment not found.")

            patient_data = drchrono_api.get_patient(access_token, appointment_data['patient'])
            if patient_data is None:
                raise Http404("Patient not found.")

            elapsed_time = int((datetime.datetime.utcnow().replace(tzinfo=utc) - appt.check_in).total_seconds()/60)
            appointments.append({
                'id': appt.id,
                'scheduled_time': conv_time(appointment_data['scheduled_time'][-8:-3]),
                'elapsed_time': elapsed_time,
                'patient_name': "{} {}".format(patient_data['first_name'], patient_data['last_name']),
                'patient_photo': patient_data['patient_photo'],
            })

        # calculate average wait time
        wait_times = []
        today_wait_times = []
        for appt in Appointment.objects.all():
            seen_time = appt.seen if appt.seen is not None else datetime.datetime.utcnow().replace(tzinfo=utc)
            elapsed_time = (seen_time - appt.check_in).total_seconds() / 60
            wait_times.append(elapsed_time)
            if seen_time.date() == datetime.datetime.today().date():
                today_wait_times.append(elapsed_time)
        avg_wait_time = int(sum(wait_times)/len(wait_times)) if len(wait_times) > 0 else 0
        avg_wait_time_today = int(sum(today_wait_times)/len(today_wait_times)) if len(today_wait_times) > 0 else 0

        return render(
            request,
            self.template,
            {
                'appointments': appointments,
                'avg_wait_time': avg_wait_time,
                'num_averaged': len(wait_times),
                'avg_wait_time_today': avg_wait_time_today,
            })

    def post(self, request):
        """process patient"""
        form = DoctorWaitlistForm(request.POST)
        if form.is_valid():  # use the form to clean input
            appt = Appointment.objects.get(id=form.cleaned_data['model_id'])
            appt.seen = datetime.datetime.utcnow().replace(tzinfo=utc)
            appt.save()

            # TODO Should this be changing anything on the API?

        return HttpResponseRedirect(reverse('d_waitlist'))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)


class Home(View):
    """Login if not logged in already, otherwise redirect to device choice screen"""
    def get(self, request):
        if not request.user.is_anonymous():
            return HttpResponseRedirect(reverse('begin'))
        return render(request, "index.html")


class Logout(View):
    """Logs out user"""
    def get(self, request):
        auth_logout(request)
        return HttpResponseRedirect(reverse('home'))

import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout

import requests

from .forms import PatientCheckinForm, DemographicsForm
from .settings import DRCHRONO_API_BASE
from .models import Appointment


def appt(request):
    access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]
    response = requests.get(
        DRCHRONO_API_BASE + 'appointments',
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
        }, params={
            'date': str(datetime.date.today()),
        })
    data = response.json()

    def conv_time(time_str):
        hr = int(time_str[:2])
        mn = int(time_str[4:])
        suffix = "PM" if hr >= 12 else "AM"
        if hr > 12:
            hr = hr % 12
        return "{}:{:02d} {}".format(hr, mn, suffix)

    # TODO filter to remove arrived appointments
    appts = [
        {'id': i['id'], 'patient': i['patient'], 'time':conv_time(i['scheduled_time'][-8:-3])}
        for i
        in data['results']
        if i['status'] == '']
    return render(request, 'appointments.html', {'appts': appts})


def patient_checkin(request, appt_id, patient_id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PatientCheckinForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # look up the user
            access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]
            response = requests.get(
                DRCHRONO_API_BASE + 'patients/{}'.format(patient_id),
                headers={
                    'Authorization': 'Bearer {}'.format(access_token),
                })
            # , params={
            #         'first_name': form.cleaned_data['first_name'],
            #         'last_name': form.cleaned_data['last_name'],
            #         'social_security_number': form.cleaned_data['ssn']
            #     })
            data = response.json()
            print(data)

            fields = ('first_name', 'last_name', 'social_security_number')
            for i in fields:
                if len(data[i]) > 0 and form.cleaned_data[i].lower() != data[i].lower():
                    form.add_error(i, 'Patient info on file does not match.')

            # # ensure lookup found a patient
            # if len(data['results']) > 1:
            #     form.add_error(None, 'Multiple users found, be more specific!')
            # elif len(data['results']) == 0:
            #     form.add_error(None, 'No Patient Found.')
            # else:

            if len(form.errors) == 0:
                return HttpResponseRedirect(reverse('demog', args=[appt_id, patient_id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PatientCheckinForm()

    return render(
        request,
        'patient_login.html',
        {'form': form})


def demographics(request, appt_id, patient_id):
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


def check_in(request, appt_id):
    """sets appointment status to arrived

    sets arrival time for appointment in database
    """

    # TODO put appt_id to arrival

    # create entry in database
    appt = Appointment.objects.create(appointment_id=appt_id)
    appt.save()

    return render(
        request,
        'checkin.html')


def waitlist(request):
    """Handles the doctor-facing waitlist

    * calculates average wait time
    * lists currently waiting patients
    * allows doctors to mark patients as "seen"
    """
    return render(
        request,
        'd_waitlist.html')


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))

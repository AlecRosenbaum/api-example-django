from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import requests

from .forms import PatientCheckinForm
from .settings import DRCHRONO_API_BASE


def patient_checkin(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PatientCheckinForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]

            response = requests.get(DRCHRONO_API_BASE + 'patients', headers={
                'Authorization': 'Bearer {}'.format(access_token),
            }, params={
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'social_security_number': form.cleaned_data['ssn']
            })
            data = response.json()
            print(data['results'])

            if len(data['results']) > 1:
                form.add_error(None, 'Multiple users found, be more specific!')
            elif len(data['results']) == 0:
                form.add_error(None, 'No Patient Found.')
            else:
                return HttpResponseRedirect(reverse('demog'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PatientCheckinForm()

    return render(request, 'patient_login.html', {'form': form})


def demographics(request, patient_id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PatientCheckinForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            access_token = request.user.social_auth.get(provider="drchrono").extra_data["access_token"]

            response = requests.get(DRCHRONO_API_BASE + 'patients', headers={
                'Authorization': 'Bearer {}'.format(access_token),
            }, params={
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'social_security_number': form.cleaned_data['ssn']
            })
            data = response.json()
            print(data['results'])

            if len(data['results']) > 1:
                form.add_error(None, 'Multiple users found, be more specific!')
            elif len(data['results']) == 0:
                form.add_error(None, 'No Patient Found.')
            else:
                return HttpResponseRedirect(reverse('demog'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PatientCheckinForm()

    return render(request, 'demographic.html', {'form': form})

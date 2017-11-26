from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import PatientCheckinForm


def patient_checkin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PatientCheckinForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('demog'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PatientCheckinForm()

    return render(request, 'patient_login.html', {'form': form})

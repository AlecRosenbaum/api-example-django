from django import forms


class PatientCheckinForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    ssn = forms.CharField(label='SSN', max_length=9)

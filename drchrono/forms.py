from django import forms


class PatientCheckinForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    ssn = forms.CharField(label='SSN', max_length=9, required=False)


GENDERS = (
    'blank',
    'Male',
    'Female'
)
RACE = (
    'blank',
    'American Indian or Alaska Native',
    'Asian',
    'Black or African American',
    'Native Hawaiian or Other Pacific Islander',
    'White',
    'Some Other Race',
)
ETHNICITY = (
    'blank',
    'Hispanic or Latino',
    'Non-Hispanic or Latino',
)
LANGUAGES = (
    'blank',
    'English',
    'Spanish',
)
STATES = (
    'AK', 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
    'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
)


class DemographicsForm(forms.Form):
    # 'first_name': 'Michelle',
    first_name = forms.CharField(label='First Name', max_length=100)
    # 'middle_name': '',
    middle_name = forms.CharField(label='Middle Name', max_length=100, required=False)
    # 'last_name': 'Harris',
    last_name = forms.CharField(label='Last Name', max_length=100)
    # 'nick_name': '',
    nick_name = forms.CharField(label='Nick Name', max_length=100, required=False)
    # 'date_of_birth': '1995-10-14',
    date_of_birth = forms.DateField(label='Date of Birth')
    # 'gender': 'Female',
    gender = forms.ChoiceField(label='Gender', choices=GENDERS)
    # 'social_security_number': '',
    ssn = forms.CharField(label='SSN', max_length=9, required=False)
    # 'race': 'blank',
    race = forms.ChoiceField(label='Race', choices=RACE)
    # 'ethnicity': 'blank',
    ethnicity = forms.ChoiceField(label='Ethnicity', choices=ETHNICITY)
    # 'preferred_language': 'blank',
    preferred_language = forms.ChoiceField(label='Preferred Language', choices=LANGUAGES)
    # 'home_phone': '',
    home_phone = forms.CharField(label='Home Phone', max_length=10, required=False)
    # 'cell_phone': '',
    cell_phone = forms.CharField(label='Cell Phone', max_length=10, required=False)
    # 'office_phone': '',
    office_phone = forms.CharField(label='Work Phone', max_length=10, required=False)
    # 'email': '',
    email = forms.EmailField(label='Email')
    # 'address': '',
    address = forms.CharField(label='Address', max_length=100, required=False)
    # 'city': '',
    city = forms.CharField(label='City', max_length=100, required=False)
    # 'state': '',
    state = forms.ChoiceField(label='State', choices=STATES)
    # 'zip_code': '',
    zip_code = forms.CharField(label='Zip Code', max_length=5, required=False)
    # 'emergency_contact_name': '',
    # 'emergency_contact_phone': '',
    # 'emergency_contact_relation': '',
    # 'employer': '',
    # 'employer_address': '',
    # 'employer_city': '',
    # 'employer_state': '',
    # 'employer_zip_code': '',
    # 'primary_care_physician': '',
    # 'responsible_party_name': '',
    # 'responsible_party_relation': '',
    # 'responsible_party_phone': '',
    # 'responsible_party_email': '',

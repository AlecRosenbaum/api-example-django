from django import forms


class PatientCheckinForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    social_security_number = forms.CharField(label='SSN', max_length=11, required=False)


GENDERS = (
    ('blank', '',),
    ('Male', 'Male',),
    ('Female', 'Female'),
    ('Other', 'Other'),
)
RACE = (
    ('blank', '',),
    ('indian', 'American Indian or Alaska Native',),
    ('asian', 'Asian',),
    ('black', 'Black or African American',),
    ('hawaiian', 'Native Hawaiian or Other Pacific Islander',),
    ('white', 'White',),
    ('declined', 'Decline to Respond',),
)
ETHNICITY = (
    ('blank', '',),
    ('hispanic', 'Hispanic or Latino',),
    ('not_hispanic', 'Non-Hispanic or Latino',),
    ('declined', 'Decline to Respond',),
)
LANGUAGES = (
    ('', '',),
    ('eng', 'English',),
    ('spa', 'Spanish',),
)
STATES = (
    ('', ''),
    ('AK', 'AK'), ('AL', 'AL'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'),
    ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'),
    ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'),
    ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'),
    ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'),
    ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'),
    ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'),
    ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'),
    ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'),
    ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY'),
)


class DemographicsForm(forms.Form):
    # doctor id
    doctor = forms.IntegerField(widget=forms.HiddenInput(), required=False)
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
    social_security_number = forms.CharField(label='SSN', max_length=11, required=False)
    # 'race': 'blank',
    race = forms.ChoiceField(label='Race', choices=RACE, required=False)
    # 'ethnicity': 'blank',
    ethnicity = forms.ChoiceField(label='Ethnicity', choices=ETHNICITY, required=False)
    # 'preferred_language': 'blank',
    preferred_language = forms.ChoiceField(label='Preferred Language', choices=LANGUAGES, required=False)
    # 'home_phone': '',
    home_phone = forms.CharField(label='Home Phone', max_length=15, required=False)
    # 'cell_phone': '',
    cell_phone = forms.CharField(label='Cell Phone', max_length=15, required=False)
    # 'office_phone': '',
    office_phone = forms.CharField(label='Work Phone', max_length=15, required=False)
    # 'email': '',
    email = forms.EmailField(label='Email', required=False)
    # 'address': '',
    address = forms.CharField(label='Address', max_length=100, required=False)
    # 'city': '',
    city = forms.CharField(label='City', max_length=100, required=False)
    # 'state': '',
    state = forms.ChoiceField(label='State', choices=STATES, required=False)
    # 'zip_code': '',
    zip_code = forms.CharField(label='Zip Code', max_length=5, required=False)
    # 'emergency_contact_name': '',
    emergency_contact_name = forms.CharField(label='Emergency Contact Name', max_length=255, required=False)
    # 'emergency_contact_phone': '',
    emergency_contact_phone = forms.CharField(label='Emergency Conatct Phone', max_length=15, required=False)
    # 'emergency_contact_relation': '',
    emergency_contact_relation = forms.CharField(label='Emergency Contact Relation', max_length=100, required=False)
    # 'employer': '',
    employer = forms.CharField(label='Employer', max_length=255, required=False)
    # 'employer_address': '',
    employer_address = forms.CharField(label='Employer Address', max_length=100, required=False)
    # 'employer_city': '',
    employer_city = forms.CharField(label='Employer City', max_length=100, required=False)
    # 'employer_state': '',
    employer_state = forms.ChoiceField(label='Employer State', choices=STATES, required=False)
    # 'employer_zip_code': '',
    employer_zip_code = forms.CharField(label='Emplyer Zip Code', max_length=5, required=False)
    # 'primary_care_physician': '',
    primary_care_physician = forms.CharField(label='Primary Care Physician', max_length=255, required=False)
    # 'responsible_party_name': '',
    responsible_party_name = forms.CharField(label='Responsible Party Name', max_length=255, required=False)
    # 'responsible_party_relation': '',
    responsible_party_relation = forms.CharField(label='Responsible Party Relation', max_length=100, required=False)
    # 'responsible_party_phone': '',
    responsible_party_phone = forms.CharField(label='Responsible Party Phone', max_length=15, required=False)
    # 'responsible_party_email': '',
    responsible_party_email = forms.EmailField(label='Responsible Party Email', required=False)

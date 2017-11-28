from django import forms


ONCLICK_SPEAK = 'responsiveVoice.speak($("label[for=\'" + this.getAttribute(\'id\') + "\']").html());'
ONINPUT_SPEAK = 'responsiveVoice.speak(this.value);'


class PatientCheckinForm(forms.Form):
    """patient confirmation form"""
    first_name = forms.CharField(label='First Name', max_length=100)
    first_name.widget.attrs['onfocus'] = ONCLICK_SPEAK
    first_name.widget.attrs['oninput'] = ONINPUT_SPEAK

    last_name = forms.CharField(label='Last Name', max_length=100)
    last_name.widget.attrs['onfocus'] = ONCLICK_SPEAK
    last_name.widget.attrs['oninput'] = ONINPUT_SPEAK

    social_security_number = forms.CharField(label='Social Security Number', max_length=11, required=False)
    social_security_number.widget.attrs['class'] = 'input-ssn'
    social_security_number.widget.attrs['onfocus'] = ONCLICK_SPEAK
    # social_security_number.widget.attrs['oninput'] = ONINPUT_SPEAK


# some choices for the demographics form
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
    """demographics entry form - comments contain example data"""
    # doctor id
    doctor = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    doctor.widget.attrs['onfocus'] = ONCLICK_SPEAK
    doctor.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'first_name': 'Michelle',
    first_name = forms.CharField(label='First Name', max_length=100)
    first_name.widget.attrs['onfocus'] = ONCLICK_SPEAK
    first_name.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'middle_name': '',
    middle_name = forms.CharField(label='Middle Name', max_length=100, required=False)
    middle_name.widget.attrs['onfocus'] = ONCLICK_SPEAK
    middle_name.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'last_name': 'Harris',
    last_name = forms.CharField(label='Last Name', max_length=100)
    last_name.widget.attrs['onfocus'] = ONCLICK_SPEAK
    last_name.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'nick_name': '',
    nick_name = forms.CharField(label='Nick Name', max_length=100, required=False)
    nick_name.widget.attrs['onfocus'] = ONCLICK_SPEAK
    nick_name.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'date_of_birth': '1995-10-14',
    date_of_birth = forms.DateField(label='Date of Birth')
    date_of_birth.widget.attrs['class'] = 'input-date'
    date_of_birth.widget.attrs['onfocus'] = ONCLICK_SPEAK
    date_of_birth.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'gender': 'Female',
    gender = forms.ChoiceField(label='Gender', choices=GENDERS)
    gender.widget.attrs['onfocus'] = ONCLICK_SPEAK
    gender.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'social_security_number': '',
    social_security_number = forms.CharField(label='Social Security Number', max_length=11, required=False)
    social_security_number.widget.attrs['class'] = 'input-ssn'
    social_security_number.widget.attrs['onfocus'] = ONCLICK_SPEAK
    # social_security_number.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'race': 'blank',
    race = forms.ChoiceField(label='Race', choices=RACE, required=False)
    race.widget.attrs['onfocus'] = ONCLICK_SPEAK
    race.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'ethnicity': 'blank',
    ethnicity = forms.ChoiceField(label='Ethnicity', choices=ETHNICITY, required=False)
    ethnicity.widget.attrs['onfocus'] = ONCLICK_SPEAK
    ethnicity.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'preferred_language': 'blank',
    preferred_language = forms.ChoiceField(label='Preferred Language', choices=LANGUAGES, required=False)
    preferred_language.widget.attrs['onfocus'] = ONCLICK_SPEAK
    preferred_language.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'home_phone': '',
    home_phone = forms.CharField(label='Home Phone', max_length=15, required=False)
    home_phone.widget.attrs['class'] = 'input-home-phone'
    home_phone.widget.attrs['onfocus'] = ONCLICK_SPEAK
    home_phone.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'cell_phone': '',
    cell_phone = forms.CharField(label='Cell Phone', max_length=15, required=False)
    cell_phone.widget.attrs['class'] = 'input-cell-phone'
    cell_phone.widget.attrs['onfocus'] = ONCLICK_SPEAK
    cell_phone.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'office_phone': '',
    office_phone = forms.CharField(label='Work Phone', max_length=15, required=False)
    office_phone.widget.attrs['class'] = 'input-work-phone'
    office_phone.widget.attrs['onfocus'] = ONCLICK_SPEAK
    office_phone.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'email': '',
    email = forms.EmailField(label='Email', required=False)
    email.widget.attrs['onfocus'] = ONCLICK_SPEAK
    email.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'address': '',
    address = forms.CharField(label='Address', max_length=100, required=False)
    address.widget.attrs['onfocus'] = ONCLICK_SPEAK
    address.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'city': '',
    city = forms.CharField(label='City', max_length=100, required=False)
    city.widget.attrs['onfocus'] = ONCLICK_SPEAK
    city.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'state': '',
    state = forms.ChoiceField(label='State', choices=STATES, required=False)
    state.widget.attrs['onfocus'] = ONCLICK_SPEAK
    state.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'zip_code': '',
    zip_code = forms.CharField(label='Zip Code', max_length=5, required=False)
    zip_code.widget.attrs['onfocus'] = ONCLICK_SPEAK
    zip_code.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'emergency_contact_name': '',
    emergency_contact_name = forms.CharField(label='Emergency Contact Name', max_length=255, required=False)
    emergency_contact_name.widget.attrs['onfocus'] = ONCLICK_SPEAK
    emergency_contact_name.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'emergency_contact_phone': '',
    emergency_contact_phone = forms.CharField(label='Emergency Conatct Phone', max_length=15, required=False)
    emergency_contact_phone.widget.attrs['class'] = 'input-emergency-phone'
    emergency_contact_phone.widget.attrs['onfocus'] = ONCLICK_SPEAK
    emergency_contact_phone.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'emergency_contact_relation': '',
    emergency_contact_relation = forms.CharField(label='Emergency Contact Relation', max_length=100, required=False)
    emergency_contact_relation.widget.attrs['onfocus'] = ONCLICK_SPEAK
    emergency_contact_relation.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'employer': '',
    employer = forms.CharField(label='Employer', max_length=255, required=False)
    employer.widget.attrs['onfocus'] = ONCLICK_SPEAK
    employer.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'employer_address': '',
    employer_address = forms.CharField(label='Employer Address', max_length=100, required=False)
    employer_address.widget.attrs['onfocus'] = ONCLICK_SPEAK
    employer_address.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'employer_city': '',
    employer_city = forms.CharField(label='Employer City', max_length=100, required=False)
    employer_city.widget.attrs['onfocus'] = ONCLICK_SPEAK
    employer_city.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'employer_state': '',
    employer_state = forms.ChoiceField(label='Employer State', choices=STATES, required=False)
    employer_state.widget.attrs['onfocus'] = ONCLICK_SPEAK
    employer_state.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'employer_zip_code': '',
    employer_zip_code = forms.CharField(label='Emplyer Zip Code', max_length=5, required=False)
    employer_zip_code.widget.attrs['onfocus'] = ONCLICK_SPEAK
    employer_zip_code.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'primary_care_physician': '',
    primary_care_physician = forms.CharField(label='Primary Care Physician', max_length=255, required=False)
    primary_care_physician.widget.attrs['onfocus'] = ONCLICK_SPEAK
    primary_care_physician.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'responsible_party_name': '',
    responsible_party_name = forms.CharField(label='Responsible Party Name', max_length=255, required=False)
    responsible_party_name.widget.attrs['onfocus'] = ONCLICK_SPEAK
    responsible_party_name.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'responsible_party_relation': '',
    responsible_party_relation = forms.CharField(label='Responsible Party Relation', max_length=100, required=False)
    responsible_party_relation.widget.attrs['onfocus'] = ONCLICK_SPEAK
    responsible_party_relation.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'responsible_party_phone': '',
    responsible_party_phone = forms.CharField(label='Responsible Party Phone', max_length=15, required=False)
    responsible_party_phone.widget.attrs['class'] = 'input-responsible-phone'
    responsible_party_phone.widget.attrs['onfocus'] = ONCLICK_SPEAK
    responsible_party_phone.widget.attrs['oninput'] = ONINPUT_SPEAK

    # 'responsible_party_email': '',
    responsible_party_email = forms.EmailField(label='Responsible Party Email', required=False)
    responsible_party_email.widget.attrs['onfocus'] = ONCLICK_SPEAK
    responsible_party_email.widget.attrs['oninput'] = ONINPUT_SPEAK


class DoctorWaitlistForm(forms.Form):
    model_id = forms.IntegerField()

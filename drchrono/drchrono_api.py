import datetime

import requests

from .settings import DRCHRONO_API_BASE


def get_todays_appointments(access_token):
    """return all appointments scheduled for today"""
    response = requests.get(
        DRCHRONO_API_BASE + 'appointments',
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
        }, params={
            'date': str(datetime.date.today()),
        })
    if 200 <= response.status_code < 400:
        return response.json()
    else:
        print(response)
        raise Exception('API returned an error response')


def get_appointment(access_token, appointment_id):
    response = requests.get(
        DRCHRONO_API_BASE + 'appointments/{}'.format(appointment_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
        })
    if 200 <= response.status_code < 400:
        return response.json()
    else:
        return None


def put_appointment(access_token, appointment_id, data):
    response = requests.put(
        DRCHRONO_API_BASE + 'appointments/{}'.format(appointment_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
        },
        data=data)
    return response


def get_patient(access_token, patient_id):
    response = requests.get(
        DRCHRONO_API_BASE + 'patients/{}'.format(patient_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
        })
    if 200 <= response.status_code < 400:
        return response.json()
    else:
        return None


def put_patient(access_token, patient_id, data):
    return requests.put(
        DRCHRONO_API_BASE + 'patients/{}'.format(patient_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token),
        },
        data=data)

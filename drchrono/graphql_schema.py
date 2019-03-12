import datetime

import dateutil.parser
import graphene
from social_django.models import UserSocialAuth

from .endpoints import PatientEndpoint, AppointmentEndpoint, DoctorEndpoint


_access_token = None


def get_token():
    """
    Social Auth module is configured to store our access tokens. This dark magic will
    fetch it for us if we've already signed in.
    """
    global _access_token
    if _access_token is None:
        oauth_provider = UserSocialAuth.objects.get(provider="drchrono")
        _access_token = oauth_provider.extra_data["access_token"]

    return _access_token


patients_api = PatientEndpoint(access_token=get_token())
doctors_api = DoctorEndpoint(access_token=get_token())
appointment_api = AppointmentEndpoint(access_token=get_token())


class Patient(graphene.ObjectType):
    id = graphene.NonNull(graphene.ID)
    date_of_birth = graphene.NonNull(graphene.String)
    doctor = graphene.NonNull(graphene.String)
    email = graphene.String()
    name = graphene.NonNull(graphene.String)
    social_security_number = graphene.String()

    @classmethod
    def from_api_response(cls, response_json):
        return cls(
            id=response_json["id"],
            date_of_birth=response_json["date_of_birth"],
            doctor=response_json["doctor"],
            email=response_json["email"],
            name="{} {}".format(response_json["first_name"], response_json["last_name"]),
            social_security_number=response_json["social_security_number"],
        )


class Doctor(graphene.ObjectType):
    id = graphene.NonNull(graphene.ID)
    email = graphene.NonNull(graphene.String)
    name = graphene.NonNull(graphene.String)

    @classmethod
    def from_api_response(cls, response_json):
        return cls(
            id=response_json["id"],
            email=response_json["email"],
            name="{} {}".format(response_json["first_name"], response_json["last_name"]),
        )


class Appointment(graphene.ObjectType):
    id = graphene.NonNull(graphene.ID)
    doctor = graphene.NonNull(Doctor)
    patient = graphene.Field(Patient)
    scheduled_time = graphene.NonNull(graphene.DateTime)
    status = graphene.NonNull(graphene.String)
    color = graphene.NonNull(graphene.String)

    @classmethod
    def from_api_response(cls, response_json):
        return cls(
            id=response_json["id"],
            doctor=Doctor.from_api_response(doctors_api.fetch(id=response_json["doctor"])),
            patient=(
                response_json["patient"]
                and Patient.from_api_response(patients_api.fetch(id=response_json["patient"]))
            ),
            status=response_json["status"],
            scheduled_time=dateutil.parser.parse(response_json["scheduled_time"]),
            color=response_json["color"],
        )


class Query(graphene.ObjectType):
    patients = graphene.List(Patient)
    appointments = graphene.List(Appointment, date_of_service=graphene.Date())

    def resolve_patients(self, _info):
        return map(Patient.from_api_response, patients_api.list())

    def resolve_appointments(self, _info, date_of_service):
        if not date_of_service:
            date_of_service = datetime.date.today()
        return map(
            Appointment.from_api_response, appointment_api.list(date=date_of_service.isoformat())
        )

    def resolve_doctors(self, _info):
        return map(Doctor.from_api_response, doctors_api.list())


schema = graphene.Schema(query=Query)

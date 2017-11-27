from django.db import models


class Appointment(models.Model):
    """a very simple model to internally keep track of appointment wait times"""

    # appointment_id
    appointment_id = models.IntegerField()

    # check_in
    check_in = models.DateTimeField(auto_now_add=True)

    # seen
    seen = models.DateTimeField(null=True)

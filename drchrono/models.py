from django.db import models


class Appointment(models.Model):
    # appointment_id
    appointment_id = models.IntegerField()

    # check_in
    check_in = models.DateTimeField(auto_now_add=True)
    # seen
    seen = models.DateTimeField(null=True)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('appointment_id', models.IntegerField()),
                ('check_in', models.DateTimeField(auto_now_add=True)),
                ('seen', models.DateTimeField()),
            ],
        ),
    ]

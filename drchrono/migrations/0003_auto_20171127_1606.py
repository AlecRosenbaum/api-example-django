# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0002_auto_20171127_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='seen',
            field=models.DateTimeField(null=True),
        ),
    ]

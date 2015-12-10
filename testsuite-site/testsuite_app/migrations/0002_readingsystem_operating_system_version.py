# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testsuite_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingsystem',
            name='operating_system_version',
            field=models.CharField(null=True, blank=True, max_length=50),
        ),
    ]

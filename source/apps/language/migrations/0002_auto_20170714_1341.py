# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='status',
            field=models.BooleanField(choices=[(False, b'Deactivated'), (True, b'Active')]),
        ),
    ]

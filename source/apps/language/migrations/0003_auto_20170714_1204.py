# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0002_auto_20170713_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='status',
            field=models.BooleanField(default=False, choices=[(True, b'Active'), (False, b'Deactivated')]),
        ),
    ]

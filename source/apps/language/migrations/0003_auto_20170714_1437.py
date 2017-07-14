# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0002_auto_20170714_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='status',
            field=models.BooleanField(default=b'deact', max_length=5, choices=[(b'act', b'Active'), (b'deact', b'Deactivated')]),
        ),
    ]

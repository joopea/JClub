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
            name='name',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='language',
            name='status',
            field=models.CharField(default=b'deact', max_length=5, choices=[(b'act', b'Active'), (b'deact', b'Deactivated')]),
        ),
    ]

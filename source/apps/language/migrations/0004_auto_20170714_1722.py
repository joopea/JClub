# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0003_auto_20170714_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=15, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='language',
            name='status',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
    ]

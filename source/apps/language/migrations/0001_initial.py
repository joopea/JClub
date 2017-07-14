# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('initial', models.CharField(max_length=3)),
                ('status', models.CharField(default=b'deact', max_length=2, choices=[(b'act', b'Active'), (b'deact', b'Deactivated')])),
            ],
        ),
    ]

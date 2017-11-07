# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-10 17:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('HNApp', '0021_auto_20160509_0543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='age',
        ),
        migrations.RemoveField(
            model_name='person',
            name='known_allergies',
        ),
        migrations.RemoveField(
            model_name='person',
            name='sex',
        ),
        migrations.RemoveField(
            model_name='person',
            name='weight',
        ),
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.CharField(default='', max_length=3),
        ),
        migrations.AddField(
            model_name='patient',
            name='height',
            field=models.CharField(default='', max_length=3),
        ),
        migrations.AddField(
            model_name='patient',
            name='hospital',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admitted', to='HNApp.Hospital'),
        ),
        migrations.AddField(
            model_name='patient',
            name='known_allergies',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='patient',
            name='sex',
            field=models.CharField(default='', max_length=7),
        ),
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.CharField(default='', max_length=3),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='time',
            field=models.DateTimeField(default=datetime.date(2016, 5, 10)),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateField(default=datetime.date(2016, 5, 10)),
        ),
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.TimeField(default=datetime.datetime(2016, 5, 10, 17, 12, 42, 832994, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='date_prescribed',
            field=models.DateField(default=datetime.date(2016, 5, 10)),
        ),
    ]

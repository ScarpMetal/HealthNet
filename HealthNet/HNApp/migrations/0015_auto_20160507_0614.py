# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-07 10:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('HNApp', '0014_auto_20160507_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.TimeField(default=datetime.datetime(2016, 5, 7, 10, 14, 59, 89038, tzinfo=utc)),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-14 23:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('HNApp', '0003_message_message_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='date',
        ),
        migrations.RemoveField(
            model_name='message',
            name='time',
        ),
        migrations.AddField(
            model_name='message',
            name='date_time',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 14, 23, 45, 8, 602829, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

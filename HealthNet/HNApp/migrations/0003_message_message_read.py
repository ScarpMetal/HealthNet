# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-14 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HNApp', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_read',
            field=models.BooleanField(default=False),
        ),
    ]
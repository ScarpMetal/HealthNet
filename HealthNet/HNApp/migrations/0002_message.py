# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-14 23:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HNApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('label', models.CharField(max_length=30)),
                ('message', models.TextField()),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_received', to='HNApp.Person')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to='HNApp.Person')),
            ],
        ),
    ]

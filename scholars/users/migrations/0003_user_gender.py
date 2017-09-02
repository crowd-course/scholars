# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170802_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('unknown', 'Unknown'), ('male', 'Male'), ('female', 'Female')], default='unknown', max_length=8),
        ),
    ]

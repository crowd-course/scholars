# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 05:45
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_coursemember_dri'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='courses.Course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='num_audio',
            field=models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='course',
            name='num_dri',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='course',
            name='num_graphics',
            field=models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='course',
            name='num_presentation',
            field=models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='course',
            name='num_scripting',
            field=models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]

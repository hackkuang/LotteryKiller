# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-04 14:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-time',),
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.PositiveIntegerField()),
                ('red1', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(33)])),
                ('red2', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(33)])),
                ('red3', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(33)])),
                ('red4', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(33)])),
                ('red5', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(33)])),
                ('red6', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(33)])),
                ('blue', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(16)])),
            ],
            options={
                'ordering': ('-period',),
            },
        ),
        migrations.AddField(
            model_name='record',
            name='begin_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_begin', to='killer.Result'),
        ),
        migrations.AddField(
            model_name='record',
            name='end_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_end', to='killer.Result'),
        ),
    ]
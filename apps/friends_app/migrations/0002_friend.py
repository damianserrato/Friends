# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-30 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('confirm', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('users', models.ManyToManyField(related_name='friends', to='friends_app.User')),
            ],
        ),
    ]

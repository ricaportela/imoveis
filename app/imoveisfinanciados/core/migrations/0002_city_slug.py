# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-27 15:45
from __future__ import unicode_literals

import uuid

import autoslug.fields
from django.db import migrations
from imoveisfinanciados.core.models import City


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='meu-slug', editable=False, populate_from='name'),
            preserve_default=False,
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-27 17:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='descritpion',
            new_name='description',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 17:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0018_auto_20170606_1249'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plan',
            options={'ordering': ['unidad_duración', 'duración']},
        ),
    ]

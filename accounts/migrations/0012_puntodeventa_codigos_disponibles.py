# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-06-28 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20190626_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntodeventa',
            name='codigos_disponibles',
            field=models.IntegerField(default=0),
        ),
    ]

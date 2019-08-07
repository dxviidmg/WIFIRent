# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-08-07 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_puntodeventa_porcentaje_comision'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntodeventa',
            name='tecnologia_wifi',
            field=models.CharField(choices=[('Unifi', 'Unifi'), ('Mikrotik', 'Mikrotik')], default='Unifi', max_length=10),
        ),
    ]

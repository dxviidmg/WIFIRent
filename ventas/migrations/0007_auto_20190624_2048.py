# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-06-25 01:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_auto_20170606_1300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venta',
            options={'ordering': ['fecha_hora']},
        ),
        migrations.RenameField(
            model_name='venta',
            old_name='fecha',
            new_name='fecha_hora',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='vendedor',
        ),
    ]

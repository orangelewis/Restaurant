# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 08:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_auto_20170601_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_item',
            name='num_item',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0019_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='photo_item',
            field=models.ImageField(upload_to='image'),
        ),
    ]

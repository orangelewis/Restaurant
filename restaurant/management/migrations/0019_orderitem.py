# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 02:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0018_auto_20170602_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_OI', models.CharField(max_length=128)),
                ('item_total', models.IntegerField(default=0)),
                ('id_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.Item')),
                ('id_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.Order')),
            ],
        ),
    ]

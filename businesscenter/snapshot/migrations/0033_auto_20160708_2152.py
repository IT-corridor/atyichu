# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 13:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapshot', '0032_auto_20160708_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ('pk',), 'verbose_name': 'Photo', 'verbose_name_plural': 'Photos'},
        ),
    ]

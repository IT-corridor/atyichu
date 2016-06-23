# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-17 12:11
from __future__ import unicode_literals

from django.db import migrations, models
import utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('snapshot', '0018_auto_20160617_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='thumb',
            field=models.ImageField(blank=True, null=True, upload_to=utils.utils.UploadPath('mirror/photo/thumbs', None, 'thumb', 'visitor'), verbose_name='Thumbnail'),
        ),
    ]
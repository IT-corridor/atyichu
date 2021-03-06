# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 16:06
from __future__ import unicode_literals

import catalog.validators
from django.db import migrations, models
import django.db.models.deletion
import utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Store', verbose_name='Store')),
            ],
            options={
                'ordering': ('priority',),
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Store', verbose_name='Store')),
            ],
            options={
                'ordering': ('priority',),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('html', models.CharField(blank=True, max_length=7, verbose_name='Html code')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Store', verbose_name='Store')),
            ],
            options={
                'ordering': ('priority',),
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colors',
            },
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Title')),
                ('year', models.CharField(max_length=4, verbose_name='Year')),
                ('season', models.CharField(choices=[('0', 'Winter'), ('1', 'Spring'), ('2', 'Summer'), ('3', 'Autumn')], max_length=1, verbose_name='Season')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Brand', verbose_name='Brand')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Color', verbose_name='Color')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Commodity',
                'verbose_name_plural': 'Commodities',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=utils.utils.UploadPath('gallery', 'commodity'), validators=[catalog.validators.SizeValidator(2)], verbose_name='Photo')),
                ('thumb', models.ImageField(upload_to=utils.utils.UploadPath('gallery/thumbs', 'commodity', suff='thumb'), verbose_name='Thumbnail')),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Commodity', verbose_name='Commodity')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Gallery',
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Category', verbose_name='Category')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Store', verbose_name='Store')),
            ],
            options={
                'ordering': ('priority',),
                'verbose_name': 'Kind',
                'verbose_name_plural': 'Kinds',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Store', verbose_name='Store')),
            ],
            options={
                'ordering': ('priority',),
                'verbose_name': 'Size',
                'verbose_name_plural': 'Sizes',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Commodity', verbose_name='Commodity')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='commodity',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Kind', verbose_name='Kind'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Size', verbose_name='Size'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Store', verbose_name='Store'),
        ),
    ]

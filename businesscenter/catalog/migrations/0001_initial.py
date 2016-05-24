# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.utils
import catalog.validators


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=50)),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('store', models.ForeignKey(verbose_name='Store', to='account.Store')),
            ],
            options={
                'verbose_name_plural': 'Brands',
                'verbose_name': 'Brand',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=50)),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('store', models.ForeignKey(verbose_name='Store', to='account.Store')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=50)),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('html', models.CharField(verbose_name='Html code', max_length=7)),
                ('store', models.ForeignKey(verbose_name='Store', to='account.Store')),
            ],
            options={
                'verbose_name_plural': 'Colors',
                'verbose_name': 'Color',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=100, blank=True)),
                ('year', models.CharField(verbose_name='Year', max_length=4)),
                ('season', models.CharField(verbose_name='Season', choices=[('0', 'Winter'), ('1', 'Spring'), ('2', 'Summer'), ('3', 'Autumn')], max_length=1)),
                ('add_date', models.DateTimeField(verbose_name='Date added', auto_now_add=True)),
                ('modify_date', models.DateTimeField(verbose_name='Date modified', auto_now=True)),
                ('brand', models.ForeignKey(verbose_name='Brand', to='catalog.Brand')),
            ],
            options={
                'verbose_name_plural': 'Commodities',
                'verbose_name': 'Commodity',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('photo', models.ImageField(verbose_name='Photo', upload_to=utils.utils.UploadPath('gallery', 'commodity'), validators=[catalog.validators.SizeValidator(2)])),
                ('thumb', models.ImageField(upload_to=utils.utils.UploadPath('gallery/thumbs', 'commodity', suff='thumb'), verbose_name='Thumbnail')),
                ('commodity', models.ForeignKey(verbose_name='Commodity', to='catalog.Commodity')),
            ],
            options={
                'verbose_name_plural': 'Gallery',
                'verbose_name': 'Gallery',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=50)),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('category', models.ForeignKey(verbose_name='Category', to='catalog.Category')),
                ('store', models.ForeignKey(verbose_name='Store', to='account.Store')),
            ],
            options={
                'verbose_name_plural': 'Kinds',
                'verbose_name': 'Kind',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=50)),
                ('priority', models.PositiveSmallIntegerField(default=0, verbose_name='Priority')),
                ('store', models.ForeignKey(verbose_name='Store', to='account.Store')),
            ],
            options={
                'verbose_name_plural': 'Sizes',
                'verbose_name': 'Size',
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=100, blank=True)),
                ('color', models.ForeignKey(verbose_name='Color', to='catalog.Color')),
                ('commodity', models.ForeignKey(verbose_name='Commodity', to='catalog.Commodity')),
                ('size', models.ForeignKey(verbose_name='Size', to='catalog.Size')),
            ],
            options={
                'verbose_name_plural': 'Stocks',
                'verbose_name': 'Stock',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=50)),
                ('commodity', models.ForeignKey(verbose_name='Commodity', to='catalog.Commodity')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='commodity',
            name='kind',
            field=models.ForeignKey(verbose_name='Kind', to='catalog.Kind'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='store',
            field=models.ForeignKey(verbose_name='Store', to='account.Store'),
        ),
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together=set([('commodity', 'color', 'size')]),
        ),
    ]

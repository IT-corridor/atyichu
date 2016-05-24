# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(db_index=True, verbose_name='Title', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'verbose_name': 'City',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(db_index=True, verbose_name='Title', max_length=100)),
                ('city', models.ForeignKey(verbose_name='City', to='account.City')),
            ],
            options={
                'verbose_name_plural': 'Districts',
                'verbose_name': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(db_index=True, verbose_name='Title', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'States',
                'verbose_name': 'State',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('logo', models.ImageField(upload_to='stores', null=True, verbose_name='Logo', blank=True)),
                ('street', models.CharField(verbose_name='Street', max_length=100)),
                ('build_name', models.CharField(verbose_name='Building name', max_length=50)),
                ('build_no', models.CharField(verbose_name='Building number', max_length=5)),
                ('apt', models.CharField(verbose_name='Apartments', max_length=5)),
                ('brand_name', models.CharField(verbose_name='Brand name', max_length=50)),
                ('district', models.ForeignKey(verbose_name='District', to='account.District')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('avatar', models.ImageField(upload_to='vendors', null=True, verbose_name='Avatar', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Vendors',
                'verbose_name': 'Vendor',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='store',
            name='owner',
            field=models.OneToOneField(to='account.Vendor', verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(verbose_name='State', to='account.State'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_created=True, verbose_name='Create date/time')),
                ('donor', models.CharField(choices=[('olx', 'olx'), ('auto.ria', 'auto.ria')], max_length=50, verbose_name='Site donor')),
                ('id_donor', models.CharField(blank=True, max_length=100, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='City')),
                ('title', models.CharField(blank=True, max_length=250, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('link', models.URLField(blank=True, verbose_name='Link')),
                ('price', models.IntegerField(blank=True, verbose_name='Price')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Name')),
                ('sms_is_send', models.BooleanField(default=False, verbose_name='SMS')),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
        ),
    ]
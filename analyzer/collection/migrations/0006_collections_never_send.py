# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-11 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_auto_20171122_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='collections',
            name='never_send',
            field=models.BooleanField(default=True),
        ),
    ]

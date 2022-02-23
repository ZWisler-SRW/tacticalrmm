# Generated by Django 3.2.12 on 2022-02-23 15:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_remove_groups_agents'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='autojoin_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groups',
            name='autojoin_filters',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), blank=True, default=list, size=None),
        ),
    ]

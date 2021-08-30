# Generated by Django 3.2.5 on 2021-07-14 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0008_script_guid'),
        ('agents', '0038_agenthistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenthistory',
            name='script',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='history', to='scripts.script'),
        ),
        migrations.AddField(
            model_name='agenthistory',
            name='script_results',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

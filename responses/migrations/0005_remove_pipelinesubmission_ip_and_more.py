# Generated by Django 5.0.7 on 2024-08-10 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responses', '0004_remove_response_ip_response_session'),
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pipelinesubmission',
            name='ip',
        ),
        migrations.AddField(
            model_name='pipelinesubmission',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sessions.session'),
        ),
    ]

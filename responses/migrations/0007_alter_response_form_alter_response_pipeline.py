# Generated by Django 5.0.7 on 2024-08-11 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0003_alter_field_type'),
        ('responses', '0006_remove_pipelinesubmission_session_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='forms.form'),
        ),
        migrations.AlterField(
            model_name='response',
            name='pipeline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='forms.pipeline'),
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-06 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_remove_response_pipline_remove_form_pipline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='fields',
            field=models.ManyToManyField(blank=True, null=True, related_name='forms', to='forms.field'),
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0003_alter_pipline_start_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipline',
            name='start_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pipline',
            name='stop_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

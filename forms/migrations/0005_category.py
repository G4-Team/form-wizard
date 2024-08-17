# Generated by Django 5.0.7 on 2024-08-11 20:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_pipeline_number_of_views'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('forms', models.ManyToManyField(blank=True, related_name='categories', to='forms.form')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pipelines', models.ManyToManyField(blank=True, related_name='categories', to='forms.pipeline')),
            ],
        ),
    ]

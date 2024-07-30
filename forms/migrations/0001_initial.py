# Generated by Django 5.0.7 on 2024-07-30 12:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField()),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField()),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField()),
                ('description_text', models.CharField(max_length=250)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'short input include just persian chars'), (2, 'short input include just english chars'), (3, 'short input include just numbers'), (4, 'short input include just a valid email'), (5, 'short input include just a valid time like 11:11:11'), (6, 'short input include just a valid ip like 192.168.1.1'), (7, 'long input include a text'), (8, 'choose one or multiple choises'), (9, 'numeric input')])),
                ('answer_required', models.BooleanField()),
                ('error_message', models.CharField(max_length=500)),
                ('form', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fields', to='forms.form')),
            ],
        ),
        migrations.CreateModel(
            name='Pipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField()),
                ('questions_responding_duration', models.PositiveBigIntegerField(help_text='Response duration time in minutes')),
                ('start_datetime', models.DateTimeField()),
                ('stop_datetime', models.DateTimeField()),
                ('hide_previous_button', models.BooleanField()),
                ('hide_next_button', models.BooleanField()),
                ('is_private', models.BooleanField()),
                ('password', models.CharField(max_length=50, null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='form',
            name='pipline',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forms.pipline'),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('pipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.pipline')),
            ],
        ),
    ]

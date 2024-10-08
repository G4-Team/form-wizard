# Generated by Django 5.0.7 on 2024-08-11 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='forms',
        ),
        migrations.RemoveField(
            model_name='category',
            name='pipelines',
        ),
        migrations.AddField(
            model_name='form',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='forms', to='forms.category'),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='pipelines', to='forms.category'),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='description_text',
            field=models.CharField(default='desc', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pipeline',
            name='slug',
            field=models.SlugField(default='slug', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pipeline',
            name='title',
            field=models.CharField(default='title', max_length=250),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-16 12:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0002_container_spec'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='image_url',
        ),
        migrations.AddField(
            model_name='container',
            name='image',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
    ]

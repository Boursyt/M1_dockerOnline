# Generated by Django 5.1.1 on 2024-10-18 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0003_remove_container_image_url_container_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='image',
        ),
    ]
# Generated by Django 3.0.5 on 2021-05-24 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0118_auto_20210520_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livephotofeedback',
            name='live_photo',
        ),
    ]

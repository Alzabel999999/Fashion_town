# Generated by Django 3.0.5 on 2021-02-20 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_auto_20210127_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='gov_link',
        ),
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='kremlin_link',
        ),
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='obl_link',
        ),
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='ok_link',
        ),
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='virtual_reception_link',
        ),
    ]

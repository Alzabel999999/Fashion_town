# Generated by Django 3.0.5 on 2021-02-18 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20210218_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='buyer_role',
        ),
    ]
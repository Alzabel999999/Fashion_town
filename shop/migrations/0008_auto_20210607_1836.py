# Generated by Django 3.0.5 on 2021-06-07 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210607_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopconfig',
            old_name='contacts_poct_code',
            new_name='contacts_post_code',
        ),
    ]

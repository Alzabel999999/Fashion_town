# Generated by Django 3.0.5 on 2021-05-18 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0072_auto_20210420_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='thumb_size',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='thumb_size',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='thumb_size',
        ),
        migrations.RemoveField(
            model_name='mainpage',
            name='thumb_size',
        ),
        migrations.RemoveField(
            model_name='news',
            name='thumb_size',
        ),
        migrations.RemoveField(
            model_name='newsphoto',
            name='thumb_size',
        ),
        migrations.RemoveField(
            model_name='reviewphoto',
            name='thumb_size',
        ),
        migrations.RemoveField(
            model_name='sliderimage',
            name='thumb_size',
        ),
    ]
# Generated by Django 3.0.5 on 2021-02-24 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0043_reviewvideo_video_preview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewvideo',
            name='video',
        ),
        migrations.RemoveField(
            model_name='reviewvideo',
            name='video_preview',
        ),
    ]

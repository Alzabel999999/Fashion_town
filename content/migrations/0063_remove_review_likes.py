# Generated by Django 3.0.5 on 2021-03-19 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0062_review_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='likes',
        ),
    ]

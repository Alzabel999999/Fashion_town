# Generated by Django 3.0.5 on 2021-03-19 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0061_news_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='likes',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество лайков'),
        ),
    ]

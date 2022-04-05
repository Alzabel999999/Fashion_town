# Generated by Django 3.0.5 on 2021-06-29 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0024_merge_20210623_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='twitter_link',
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='telegram_link',
            field=models.CharField(blank=True, default='https://paste_link/', max_length=512, verbose_name='Ссылка Telegram'),
        ),
    ]
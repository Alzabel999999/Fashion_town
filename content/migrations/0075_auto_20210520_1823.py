# Generated by Django 3.0.5 on 2021-05-20 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0074_auto_20210520_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Название'),
        ),
    ]

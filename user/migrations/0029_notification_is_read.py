# Generated by Django 3.0.5 on 2021-03-16 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_auto_20210315_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='Прочитано'),
        ),
    ]

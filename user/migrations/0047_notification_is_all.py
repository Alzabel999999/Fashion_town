# Generated by Django 3.0.5 on 2022-02-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0046_user_is_shop_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_all',
            field=models.BooleanField(default=False, verbose_name='Всем'),
        ),
    ]
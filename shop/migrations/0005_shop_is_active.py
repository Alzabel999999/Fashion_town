# Generated by Django 3.0.5 on 2021-05-31 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_shop_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Включено'),
        ),
    ]

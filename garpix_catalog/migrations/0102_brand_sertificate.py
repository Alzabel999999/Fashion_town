# Generated by Django 3.0.5 on 2021-03-31 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0101_auto_20210330_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='sertificate',
            field=models.BooleanField(default=False, verbose_name='Сертификат'),
        ),
    ]

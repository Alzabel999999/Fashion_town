# Generated by Django 3.0.5 on 2022-04-03 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0146_auto_20220305_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='in_archive',
            field=models.BooleanField(default=False, verbose_name='В архиве'),
        ),
    ]

# Generated by Django 3.0.5 on 2022-03-05 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0145_auto_20220305_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='vendor_code',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Артикул'),
        ),
    ]

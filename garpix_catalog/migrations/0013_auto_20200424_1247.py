# Generated by Django 2.1 on 2020-04-24 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0012_auto_20200424_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='new_price',
        ),
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Старая цена'),
        ),
    ]
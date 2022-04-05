# Generated by Django 3.0.5 on 2021-04-03 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0103_remove_productsku_sku_rc'),
        ('garpix_cart_rest', '0024_cartitemspack_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitemspack',
            name='condition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='garpix_catalog.RedemptionCondition', verbose_name='Условие выкупа'),
        ),
    ]

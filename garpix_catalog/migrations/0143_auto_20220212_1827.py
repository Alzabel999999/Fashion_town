# Generated by Django 3.0.5 on 2022-02-12 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0142_remove_product_is_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_rc',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rc_products', to='garpix_catalog.RedemptionCondition', verbose_name='Условие выкупа'),
        ),
    ]
# Generated by Django 3.0.5 on 2021-04-05 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0103_remove_productsku_sku_rc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsku',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='size_skus', to='garpix_catalog.Size', verbose_name='Размер'),
        ),
    ]

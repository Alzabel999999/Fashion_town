# Generated by Django 3.0.5 on 2022-02-17 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0121_auto_20220214_2051'),
        ('purchase', '0003_auto_20210617_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='garpix_order.Order'),
        ),
    ]

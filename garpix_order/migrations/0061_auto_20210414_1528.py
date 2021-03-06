# Generated by Django 3.0.5 on 2021-04-14 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0060_auto_20210414_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionitem',
            name='order_item',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_item_collection_item', to='garpix_order.OrderItem', verbose_name='Позиция в заказе'),
        ),
    ]

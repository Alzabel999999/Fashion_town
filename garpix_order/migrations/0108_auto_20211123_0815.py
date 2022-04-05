# Generated by Django 3.0.5 on 2021-11-23 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0107_orderitem_change_agreement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_method_orders', to='garpix_order.PaymentMethod', verbose_name='Метод оплаты'),
        ),
    ]
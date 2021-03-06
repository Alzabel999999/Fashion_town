# Generated by Django 3.0.5 on 2021-03-12 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0030_orderitem_qty'),
        ('user', '0025_auto_20210312_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_payments', to='garpix_order.Order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_payments', to='user.Profile', verbose_name='Профиль'),
        ),
    ]

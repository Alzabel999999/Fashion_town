# Generated by Django 3.0.5 on 2021-05-25 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0076_auto_20210525_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Стоимость доставки')),
                ('status', models.CharField(choices=[('delivery_payment_waiting', 'Ожидается оплата'), ('delivery_payment_confirmed', 'Оплачено')], default='delivery_payment_waiting', max_length=40, verbose_name='Статус')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_delivery', to='garpix_order.Order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Доставка',
                'verbose_name_plural': 'Доставки',
                'ordering': ('-id',),
            },
        ),
    ]

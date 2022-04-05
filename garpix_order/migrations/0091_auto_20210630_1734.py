# Generated by Django 3.0.5 on 2021-06-30 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0090_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='service_orders', to='garpix_order.Service', verbose_name='Доп. услуги'),
        ),
        migrations.AddField(
            model_name='order',
            name='total_services_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Цена доп. услуг'),
        ),
    ]
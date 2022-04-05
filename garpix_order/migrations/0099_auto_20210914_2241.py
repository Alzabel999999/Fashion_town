# Generated by Django 3.0.5 on 2021-09-14 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0098_withdrawal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('payment_waiting', 'Ожидается оплата'), ('paid', 'Товар оплачен'), ('ordered', 'Товар заказан'), ('redeemed', 'Товар выкуплен'), ('packaging', 'Товар на упаковке'), ('sended', 'Товар отправлен'), ('replacement', 'Замена товара'), ('canceled', 'Отмена товара')], default='ordered', max_length=20, verbose_name='Статус'),
        ),
    ]

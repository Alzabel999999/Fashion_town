# Generated by Django 3.0.5 on 2021-07-13 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0046_user_is_shop_buyer'),
        ('garpix_order', '0092_auto_20210630_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile_payment', to='user.Profile', verbose_name='Профиль пользователя'),
        ),
    ]

# Generated by Django 3.0.5 on 2021-03-05 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_profile_shop_link'),
        ('garpix_order', '0021_auto_20210217_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryaddress',
            name='user',
        ),
        migrations.AddField(
            model_name='deliveryaddress',
            name='profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile_addresses', to='user.Profile', verbose_name='Профиль пользователя'),
            preserve_default=False,
        ),
    ]

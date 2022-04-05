# Generated by Django 3.0.5 on 2021-05-21 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0074_auto_20210520_2123'),
        ('user', '0039_auto_20210513_1155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-id'], 'verbose_name': 'Пополнение', 'verbose_name_plural': 'Пополнения'},
        ),
        migrations.RemoveField(
            model_name='payment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.AddField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='payment',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='Имя отправителя'),
        ),
        migrations.AddField(
            model_name='payment',
            name='requisites',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requisite_payments', to='garpix_order.Requisites', verbose_name='Реквизиты'),
        ),
        migrations.AddField(
            model_name='payment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='comment',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Комментарий'),
        ),
    ]
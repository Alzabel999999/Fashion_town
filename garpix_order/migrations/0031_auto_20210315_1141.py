# Generated by Django 3.0.5 on 2021-03-15 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0030_orderitem_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='passport_issue_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата выдачи'),
        ),
        migrations.AddField(
            model_name='order',
            name='passport_issued',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Кем выдан'),
        ),
        migrations.AddField(
            model_name='order',
            name='passport_number',
            field=models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='Номер'),
        ),
    ]

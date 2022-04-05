# Generated by Django 3.0.5 on 2021-03-22 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_page', '0018_auto_20210302_1557'),
        ('garpix_order', '0042_order_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='parent',
            field=models.ForeignKey(blank=True, limit_choices_to={'page_type': 29}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='garpix_page.Page', verbose_name='Родительская страница'),
        ),
    ]

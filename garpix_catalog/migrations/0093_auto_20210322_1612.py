# Generated by Django 3.0.5 on 2021-03-22 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_page', '0018_auto_20210302_1557'),
        ('garpix_catalog', '0092_auto_20210319_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livephotoalbum',
            name='parent',
            field=models.ForeignKey(blank=True, limit_choices_to={'page_type': 25}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='garpix_page.Page', verbose_name='Родительская страница'),
        ),
        migrations.AlterField(
            model_name='product',
            name='parent',
            field=models.ForeignKey(blank=True, limit_choices_to={'page_type': 5}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='garpix_page.Page', verbose_name='Родительская страница'),
        ),
    ]

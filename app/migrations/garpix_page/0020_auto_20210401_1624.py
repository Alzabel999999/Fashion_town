# Generated by Django 3.0.5 on 2021-04-01 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_page', '0019_auto_20210401_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='position',
            field=models.CharField(choices=[('DEFAULT', 'default'), ('INFO', 'Информация')], default='', max_length=100, verbose_name='Позиция'),
        ),
    ]

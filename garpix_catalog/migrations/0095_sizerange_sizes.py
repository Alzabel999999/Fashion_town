# Generated by Django 3.0.5 on 2021-03-23 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0094_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='sizerange',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='garpix_catalog.Size', verbose_name='Размеры'),
        ),
    ]

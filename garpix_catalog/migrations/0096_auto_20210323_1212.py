# Generated by Django 3.0.5 on 2021-03-23 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0095_sizerange_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sizerangepack',
            name='number_in_range',
        ),
        migrations.AddField(
            model_name='sizerangepack',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='garpix_catalog.Size', verbose_name='Размеры'),
        ),
        migrations.DeleteModel(
            name='SizeRange',
        ),
    ]

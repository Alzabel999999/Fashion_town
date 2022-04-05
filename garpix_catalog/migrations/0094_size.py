# Generated by Django 3.0.5 on 2021-03-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0093_auto_20210322_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(choices=[(0, 'one size'), (1, 'XS (34)'), (2, 'S (36)'), (3, 'M (38)'), (4, 'L (40)'), (5, 'XL (42)'), (6, '2XL (44)'), (7, '3XL (46)'), (8, '4XL (48)'), (9, '5XL (50)'), (10, '6XL (52)')], default=0, unique=True, verbose_name='Размер')),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
                'ordering': ['size'],
            },
        ),
    ]
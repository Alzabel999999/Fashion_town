# Generated by Django 3.0.5 on 2021-03-16 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0033_auto_20210315_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=60, verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ('title',),
            },
        ),
    ]
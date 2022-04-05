# Generated by Django 3.0.5 on 2021-03-25 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0003_newordersstatistic'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersStatusStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Статистика выкупленных товаров, завершенных заявок, замен и их процентное соотношение.',
            },
        ),
    ]

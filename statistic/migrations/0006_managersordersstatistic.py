# Generated by Django 3.0.5 on 2021-03-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0005_ordersintimestatistic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagersOrdersStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Статистика по каждому из менеджеров сколько единиц выкуплено/упаковано и совокупно',
            },
        ),
    ]

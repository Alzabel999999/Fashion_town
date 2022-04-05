# Generated by Django 3.0.5 on 2021-04-20 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0013_auto_20210330_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackManagersStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '06 - Статистика по каждому из менеджеров по упаковке',
            },
        ),
        migrations.CreateModel(
            name='RedeemedTimeStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '09 - Статистика по среднему количеству времени на выкуп единицы и упаковки',
            },
        ),
        migrations.CreateModel(
            name='UserShopsStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '07 - Статистика число пользователей, которые создали собственный Интернет-магазин',
            },
        ),
        migrations.AlterModelOptions(
            name='managersordersstatistic',
            options={'verbose_name': '05 - Статистика по каждому из менеджеров сколько единиц выкуплено/упаковано и совокупно'},
        ),
        migrations.AlterModelOptions(
            name='newordersstatistic',
            options={'verbose_name': '02 - Статистика по количеству заказов новых пользователей'},
        ),
        migrations.AlterModelOptions(
            name='ordersintimestatistic',
            options={'verbose_name': '03 - Статистика по общему количеству заказов'},
        ),
        migrations.AlterModelOptions(
            name='orderspercitystatistic',
            options={'verbose_name': '10 - Статистика по городам'},
        ),
        migrations.AlterModelOptions(
            name='ordersstatusstatistic',
            options={'verbose_name': '04 - Статистика по количеству выкупленных товаров, завершенных заявок, замен'},
        ),
        migrations.AlterModelOptions(
            name='overageitemsinordersstatistic',
            options={'verbose_name': '08 - Статистика по среднему количеству товаров в посылке (без опта)'},
        ),
        migrations.AlterModelOptions(
            name='registrationstatistic',
            options={'verbose_name': '01 - Статистика по количеству регистраций'},
        ),
        migrations.AlterModelOptions(
            name='revenuesumstatistic',
            options={'verbose_name': '11 - Статистика по сумме выручки'},
        ),
    ]

# Generated by Django 3.0.5 on 2021-03-18 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('content', '0054_auto_20210318_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='sites',
            field=models.ManyToManyField(blank=True, default='1', to='sites.Site', verbose_name='Сайты для отображения'),
        ),
    ]

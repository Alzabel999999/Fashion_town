# Generated by Django 3.0.5 on 2021-03-18 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('content', '0053_auto_20210304_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='sites',
            field=models.ManyToManyField(blank=True, default='1', null=True, to='sites.Site', verbose_name='Сайты для отображения'),
        ),
    ]
# Generated by Django 2.2 on 2019-04-12 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('garpix_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='sites',
            field=models.ManyToManyField(default='1', to='sites.Site', verbose_name='Сайты для отображения'),
        ),
    ]
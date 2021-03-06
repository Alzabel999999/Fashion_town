# Generated by Django 3.0.5 on 2021-02-17 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='passport_issue_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата выдачи паспорта'),
        ),
        migrations.AddField(
            model_name='profile',
            name='passport_issued',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Кем выдан паспорт'),
        ),
        migrations.AddField(
            model_name='profile',
            name='passport_number',
            field=models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='Серия и номер паспорта'),
        ),
    ]

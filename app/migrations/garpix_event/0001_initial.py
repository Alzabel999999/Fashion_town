# Generated by Django 2.1 on 2020-04-22 22:28

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='Заголовок')),
                ('event_type', models.PositiveIntegerField(choices=[(0, 'Empty Event'), (1, 'Event 1')], verbose_name='Тип')),
                ('status', django_fsm.FSMField(choices=[('created', 'CREATED'), ('pending', 'PENDING'), ('succeeded', 'SUCCEEDED'), ('cancel', 'CANCELED'), ('delayed', 'DELAYED'), ('failed', 'FAILED'), ('timeout', 'TIMEOUT')], default='created', max_length=50)),
                ('description', models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='Описание')),
                ('instance_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='Идентификатор целевого экземпляра')),
                ('event_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Данные о событии')),
                ('custom_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Пользовательские данные события')),
                ('is_locked', models.BooleanField(default=False, verbose_name='Событие заблокировано')),
                ('execution_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата исполнения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
                'ordering': ('-updated_at', '-created_at'),
            },
        ),
    ]

# Generated by Django 3.0.5 on 2022-03-20 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('garpix_order', '0126_auto_20220312_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrespondenceOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, default='', verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('order_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='correspondence_messages', to='garpix_order.OrderItem', verbose_name='Товар заказа')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_correspondence_order_items', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CorrespondenceOrderItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, default='', max_length=255, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Изображение')),
                ('image_thumb', models.CharField(blank=True, max_length=255)),
                ('correspondence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='correspondence_order_item_message_images', to='garpix_order.CorrespondenceOrderItem', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]

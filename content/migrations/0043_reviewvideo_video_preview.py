# Generated by Django 3.0.5 on 2021-02-24 13:32

from django.db import migrations, models
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0042_auto_20210220_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewvideo',
            name='video_preview',
            field=models.FileField(blank=True, default='', max_length=255, null=True, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Видео превью'),
        ),
    ]

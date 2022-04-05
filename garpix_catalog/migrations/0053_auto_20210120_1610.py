# Generated by Django 3.0.5 on 2021-01-20 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0052_auto_20210120_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livephotofeedback',
            name='live_photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='live_photo_feedbacks', to='garpix_catalog.LivePhotoImage', verbose_name='Фото'),
        ),
    ]
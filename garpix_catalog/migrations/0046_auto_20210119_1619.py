# Generated by Django 3.0.5 on 2021-01-19 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0045_auto_20210119_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='livephotofeedbackimages',
            options={'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.AlterField(
            model_name='livephotofeedback',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='garpix_catalog.LivePhotoFeedbackImages', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='livephotofeedbackimages',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Изображение'),
        ),
    ]

# Generated by Django 3.0.5 on 2021-01-20 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0049_livephotoalbum_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livephotofeedback',
            name='image',
        ),
        migrations.AddField(
            model_name='livephotofeedback',
            name='live_photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='live_photo_feedbacks', to='garpix_catalog.LivePhotoImage', verbose_name='Фото'),
        ),
        migrations.DeleteModel(
            name='LivePhotoFeedbackImages',
        ),
    ]

# Generated by Django 3.0.5 on 2021-02-16 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0076_auto_20210216_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livephotoalbum',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brand_live_photo_albums', to='garpix_catalog.Brand', verbose_name='Бренд'),
        ),
    ]

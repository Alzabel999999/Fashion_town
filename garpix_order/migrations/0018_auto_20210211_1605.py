# Generated by Django 3.0.5 on 2021-02-11 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0017_auto_20210211_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='content',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='order',
            name='page_type',
        ),
        migrations.RemoveField(
            model_name='order',
            name='seo_author',
        ),
        migrations.RemoveField(
            model_name='order',
            name='seo_description',
        ),
        migrations.RemoveField(
            model_name='order',
            name='seo_image',
        ),
        migrations.RemoveField(
            model_name='order',
            name='seo_keywords',
        ),
        migrations.RemoveField(
            model_name='order',
            name='seo_og_type',
        ),
        migrations.RemoveField(
            model_name='order',
            name='seo_title',
        ),
        migrations.RemoveField(
            model_name='order',
            name='sites',
        ),
        migrations.RemoveField(
            model_name='order',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='order',
            name='title',
        ),
    ]
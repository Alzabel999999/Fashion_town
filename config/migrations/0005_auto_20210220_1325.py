# Generated by Django 3.0.5 on 2021-02-20 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_page', '0017_auto_20210215_1110'),
        ('config', '0004_auto_20210220_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='page_type_404',
            field=models.ForeignKey(blank=True, limit_choices_to={'page_type': 32}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conf_404', to='garpix_page.Page', verbose_name='Страница 404'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='page_type_500',
            field=models.ForeignKey(blank=True, limit_choices_to={'page_type': 33}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conf_500', to='garpix_page.Page', verbose_name='Страница 500'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='page_type_catalog',
            field=models.ForeignKey(blank=True, limit_choices_to={'page_type': 5}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conf_catalog', to='garpix_page.Page', verbose_name='Страница Каталог'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='page_type_live_photos',
            field=models.ForeignKey(blank=True, limit_choices_to={'page_type': 24}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conf_live_photos', to='garpix_page.Page', verbose_name='Страница Живые фото'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='page_type_news',
            field=models.ForeignKey(blank=True, limit_choices_to={'page_type': 26}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conf_news', to='garpix_page.Page', verbose_name='Страница Новости'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='page_type_reviews',
            field=models.ForeignKey(blank=True, limit_choices_to={'page_type': 31}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conf_reviews', to='garpix_page.Page', verbose_name='Страница Отзывы'),
        ),
    ]

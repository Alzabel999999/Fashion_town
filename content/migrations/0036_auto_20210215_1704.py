# Generated by Django 3.0.5 on 2021-02-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0035_news_rubrics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='rubrics',
            field=models.ManyToManyField(blank=True, to='content.NewsRubric', verbose_name='Рубрики'),
        ),
    ]
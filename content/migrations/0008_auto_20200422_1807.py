# Generated by Django 2.1 on 2020-04-22 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20200422_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='Название тега')),
                ('title_ru', models.CharField(max_length=512, null=True, verbose_name='Название тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='tag',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='post_tags', to='content.Tag', verbose_name='Теги'),
        ),
    ]

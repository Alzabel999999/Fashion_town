# Generated by Django 3.0.5 on 2021-05-25 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0042_auto_20210521_1510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alreadysaw',
            options={'ordering': ['-id'], 'verbose_name': 'Уже смотрели', 'verbose_name_plural': 'Уже смотрели'},
        ),
    ]
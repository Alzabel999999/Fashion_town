# Generated by Django 3.0.5 on 2020-04-28 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_menu', '0003_auto_20200421_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
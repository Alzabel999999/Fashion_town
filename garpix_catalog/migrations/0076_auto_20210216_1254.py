# Generated by Django 3.0.5 on 2021-02-16 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0075_auto_20210215_1802'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='brandcategory',
            unique_together={('category', 'brand')},
        ),
        migrations.AlterUniqueTogether(
            name='productsku',
            unique_together={('product', 'size', 'color')},
        ),
    ]

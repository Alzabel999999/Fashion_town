# Generated by Django 3.0.5 on 2021-01-22 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('garpix_catalog', '0056_auto_20210122_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='redemptioncondition',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_garpix_catalog.redemptioncondition_set+', to='contenttypes.ContentType'),
        ),
    ]
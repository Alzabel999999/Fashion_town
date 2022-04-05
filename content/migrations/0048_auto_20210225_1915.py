# Generated by Django 3.0.5 on 2021-02-25 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20210225_1658'),
        ('content', '0047_auto_20210225_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AddField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_reviews', to='user.Profile', verbose_name='Профиль'),
        ),
    ]

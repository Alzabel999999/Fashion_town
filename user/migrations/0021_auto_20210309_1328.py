# Generated by Django 3.0.5 on 2021-03-09 13:28

from django.db import migrations, models
import django.db.models.deletion
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Баланс'),
        ),
        migrations.AddField(
            model_name='profile',
            name='receive_newsletter',
            field=models.BooleanField(default=True, verbose_name='Получать рассылку'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('beneficiary', models.FloatField(verbose_name='Счет получателя')),
                ('status', models.IntegerField(choices=[(0, 'Ожидается'), (1, 'Успешно')], default=0, verbose_name='Статус')),
                ('comment', models.CharField(max_length=150, verbose_name='Комментарий')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('receipt', models.FileField(upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Чек')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]

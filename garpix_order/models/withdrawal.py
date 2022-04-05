from django.db import models
from garpix_utils.file_field import get_file_path
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator


class Withdrawal(models.Model):
    processed = models.BooleanField(verbose_name='Заявка обработана', default=False, blank=True)
    summary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма вывода', null=True,
                                  validators=[
                                      RegexValidator(r'^[0-9]*$', 'Значение должно содержать только цифры'),
                                      MinLengthValidator(1),
                                      MaxLengthValidator(10),
                                  ]
                                  )
    full_name = models.CharField(max_length=126, verbose_name='ФИО получателя', null=True,
                                 validators=[
                                     RegexValidator(r'^[a-zA-Zа-яА-ЯёЁ-]*$',
                                                    'Специальные символы не допускаются, за исключением "-"'),
                                     MinLengthValidator(4),
                                     MaxLengthValidator(126),
                                 ]
                                 )
    account_number = models.IntegerField(verbose_name='№ счета получателя или карты в Банке', null=True,
                                         validators=[
                                             RegexValidator(r'^[0-9]*$', 'Значение должно содержать только цифры'),
                                             MinLengthValidator(1),
                                             MaxLengthValidator(10),
                                         ]
                                         )
    statement = models.FileField(verbose_name='Заявление', null=True, upload_to=get_file_path)
    user = models.ForeignKey('user.Profile', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='withdrawals', null=True)

    def __str__(self):
        return f'Заявка №{self.pk}, от {self.full_name}'

    class Meta:
        verbose_name = 'Заявка на вывод средств'
        verbose_name_plural = 'Заявки на вывод средств'

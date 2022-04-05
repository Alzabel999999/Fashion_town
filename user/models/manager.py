from django.db import models
from ..models import User


class Manager(models.Model):

    class MANAGER_ROLE:
        ADMIN = 1
        WAREHOUSE_MANAGER = 2
        PURCHASING_MANAGER = 3
        TYPES = (
            (ADMIN, 'Администратор'),
            (WAREHOUSE_MANAGER, 'Менеджер склада'),
            (PURCHASING_MANAGER, 'Менеджер по закупкам'),
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='manager')
    role = models.IntegerField(verbose_name='Роль', default=MANAGER_ROLE.PURCHASING_MANAGER, choices=MANAGER_ROLE.TYPES)

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'
        ordering = ('user', )

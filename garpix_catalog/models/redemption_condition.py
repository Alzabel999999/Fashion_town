from django.db import models
from polymorphic.models import PolymorphicModel
from .size import Size


class RedemptionCondition(PolymorphicModel):

    class RC_TYPE:
        BASE = 0
        RANGE = 1
        PACK = 2
        MINIMUM = 3
        TYPES = (
            (BASE, 'базовый'),
            (RANGE, 'ряд'),
            (PACK, 'пачка'),
            (MINIMUM, 'микс'),
        )

    number = models.PositiveIntegerField(verbose_name='Количество', blank=True, null=True, default=1)
    rc_type = models.PositiveIntegerField(verbose_name='Тип', choices=RC_TYPE.TYPES, default=RC_TYPE.BASE)

    class Meta:
        verbose_name = 'Условие выкупа'
        verbose_name_plural = 'Условия выкупа'

    def __str__(self):
        return str(self.get_real_instance())


class SizeRangePack(RedemptionCondition):

    sizes = models.ManyToManyField(Size, verbose_name='Размеры', blank=True)

    class Meta:
        verbose_name = 'Один или несколько размерных рядов'
        verbose_name_plural = 'Один или несколько размерных рядов'

    def get_items_count(self):
        return self.number * self.number_in_range

    def __str__(self):
        sizes = [size.get_size_name() for size in self.sizes.all()]
        if len(sizes) > 0:
            sizes = ', '.join(sizes,)
        else:
            sizes = 'Все доступные размеры'
        if self.number < 2:
            return f'Размерный ряд ({sizes})'
        return f'{self.number} размерных ряда(-ов) ({sizes})'

    def save(self, *args, **kwargs):
        self.rc_type = self.RC_TYPE.RANGE
        super(SizeRangePack, self).save()


class Pack(RedemptionCondition):

    class Meta:
        verbose_name = 'Пачка'
        verbose_name_plural = 'Пачка'

    def __str__(self):
        return f'Пачка {self.number} шт одной модели, один цвет, один размер'

    def save(self, *args, **kwargs):
        self.rc_type = self.RC_TYPE.PACK
        super(Pack, self).save()


class Minimum(RedemptionCondition):

    one_model = models.BooleanField(verbose_name='Товары одной модели', default=False)

    class Meta:
        verbose_name = 'Минимум'
        verbose_name_plural = 'Минимум'

    def __str__(self):
        if self.one_model:
            return f'{self.number} шт с одной модели (любые цвета и размеры)'
        return f'{self.number} шт с фирмы любых моделей'

    def save(self, *args, **kwargs):
        self.rc_type = self.RC_TYPE.MINIMUM
        super(Minimum, self).save()

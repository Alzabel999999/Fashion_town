from django.db import models


class Size(models.Model):

    class SIZE:
        ONE_SIZE = 0
        XS = 1
        S = 2
        M = 3
        L = 4
        XL = 5
        XXL = 6
        XXXL = 7
        XXXXL = 8
        XXXXXL = 9
        XXXXXXL = 10
        TYPES = (
            (ONE_SIZE, 'one size'),
            (XS, 'XS (34)'),
            (S, 'S (36)'),
            (M, 'M (38)'),
            (L, 'L (40)'),
            (XL, 'XL (42)'),
            (XXL, '2XL (44)'),
            (XXXL, '3XL (46)'),
            (XXXXL, '4XL (48)'),
            (XXXXXL, '5XL (50)'),
            (XXXXXXL, '6XL (52)'),
        )
        SIZES = {
            ONE_SIZE: 'one size',
            XS: 'XS',
            S: 'S',
            M: 'M',
            L: 'L',
            XL: 'XL',
            XXL: '2XL',
            XXXL: '3XL',
            XXXXL: '4XL',
            XXXXXL: '5XL',
            XXXXXXL: '6XL',
        }

    size = models.IntegerField(verbose_name='Размер', default=SIZE.ONE_SIZE, choices=SIZE.TYPES, unique=True)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['size',]

    def __str__(self):
        return self.get_size_name()

    def get_size_name(self):
        return self.SIZE.SIZES[self.size]

    def get_size_number(self):
        return self.size

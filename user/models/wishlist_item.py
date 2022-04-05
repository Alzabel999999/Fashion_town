from django.db import models
from .profile import Profile
from garpix_catalog.models import Product


class WishListItem(models.Model):

    profile = models.ForeignKey(Profile, verbose_name='Пользователь', related_name='user_wishlist_items',
                                on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Подукт', related_name='product_wishlist_items',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('profile', 'product')

    def __str__(self):
        return f'{self.profile} - {self.product}'

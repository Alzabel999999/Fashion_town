from django.db import models
from user.models import Profile
from garpix_page.abstract.mixins.content import ActiveMixin
from ..mixin import AddressMixin, ReceiverMixin


class DeliveryAddress(ActiveMixin, ReceiverMixin, AddressMixin):
    profile = models.ForeignKey(
        Profile, verbose_name='Профиль пользователя', on_delete=models.CASCADE, related_name='profile_addresses')

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return f'{self.get_full_address()} ({self.get_name_initial()})'

    def get_full_address(self):
        post = self.post_code if self.post_code else ''
        country = self.country
        city = self.city if self.city else ''
        street = self.street if self.street else ''
        house = self.house if self.house else ''
        flat = self.flat if self.flat else ''
        return f'{post} {country}, {city}, {street}, {house}, {flat}'

    def get_name_initial(self):
        first_name = f'{self.first_name[0]}.' if self.first_name else ''
        middle_name = f'{self.middle_name[0]}.' if self.middle_name else ''
        last_name = self.last_name if self.last_name else ''
        return f'{last_name} {first_name}{middle_name}'

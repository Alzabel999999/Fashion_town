from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from garpix_confirm.models import UserConfirmEmailMixin, UserConfirmPhoneMixin
from django.contrib.auth import get_user_model
from garpix_utils.strings import get_random_string
from garpix_notify.models import Notify
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re


def validator_fio(value):
    matched = re.search(r'^[a-zA-Zа-яА-ЯёЁ][a-zA-Zа-яА-ЯёЁ -]*[a-zA-Zа-яА-ЯёЁ]$', value)
    if not (matched and value == matched.group()):
        raise ValidationError(_('wrong string'))


class User(AbstractUser, UserConfirmEmailMixin, UserConfirmPhoneMixin):
    class STATUS:
        UNREGISTRED = 0
        AWAING_REGICTRATION_CONFIRM = 1
        REGISTRATION_REJECTED = 2
        REGISTRED = 3
        TYPES = (
            (UNREGISTRED, 'Незарегистрированный пользователь'),
            (AWAING_REGICTRATION_CONFIRM, 'Ожидается подтверждение регистрации'),
            (REGISTRATION_REJECTED, 'Отказ в регистрации'),
            (REGISTRED, 'Зарегистрированный пользователь'),
        )

    password_reset_key = models.CharField(max_length=64, default="", verbose_name="Код сброса пароля", blank=True)
    phone_change_key = models.CharField(max_length=64, default="", verbose_name="Код смены телефона", blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    birthdate = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='Дата рождения', blank=True, null=True)
    status = models.IntegerField(
        verbose_name='Статус пользователя', default=STATUS.AWAING_REGICTRATION_CONFIRM, choices=STATUS.TYPES)

    first_name = models.CharField(_('first name'), max_length=30, blank=True, validators=[validator_fio, ])
    middle_name = models.CharField(_('middle name'), max_length=50, blank=True, validators=[validator_fio, ])
    last_name = models.CharField(_('last name'), max_length=150, blank=True, validators=[validator_fio, ])

    is_buyer = models.BooleanField(default=False, verbose_name='Покупатель')
    is_shop_buyer = models.BooleanField(default=False, verbose_name='Покупатель дочернего ИМ')

    def send_email_confirmation_key(self, email):
        """
        Отправка письма подтверждения на Email
        1. генерируем код, отправляем емейл
        2. сохраняем значение емейла в новый, чтобы можно было поменять
        3. при подтверждении нового емейла, заменяем старый
        """
        anybody_have_this_email = get_user_model().objects.filter(
            email=email, is_email_confirmed=True).count() > 0  # Проверка на уникальность
        if not anybody_have_this_email:
            email_confirmation_key = get_random_string(64)
            self.new_email = email
            self.email_confirmation_key = email_confirmation_key
            if self.pk is not None:
                self.save()
            link = self.get_link_confirm_email()
            Notify.send(
                event=settings.CONFIRM_EMAIL_EVENT,
                context={'user': self.username, 'link': link},
                email=email
            )
            return True
        return False

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):

        return self.get_full_name() if (self.first_name and self.last_name) \
            else self.email if self.email \
            else self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_buyer:
            if not hasattr(self, 'profile'):
                from .profile import Profile
                Profile.objects.create(user=self)
            if self.status == 2:
                self.profile.role = 1
                self.profile.save()
        if self.is_staff:
            if not hasattr(self, 'manager'):
                from .manager import Manager
                Manager.objects.create(user=self)

    def set_profile_data(self, data):
        profile = self.profile
        profile.vk_link = data['vk_link'] if 'vk_link' in data.keys() else profile.vk_link
        profile.insta_link = data['insta_link'] if 'insta_link' in data.keys() else profile.insta_link
        profile.other_link = data['other_link'] if 'other_link' in data.keys() else profile.other_link
        profile.site_link = data['site_link'] if 'site_link' in data.keys() else profile.site_link
        profile.inn = data['inn'] if 'inn' in data.keys() else profile.inn
        profile.organization = data['organization'] if 'organization' in data.keys() else profile.organization
        profile.receive_newsletter = \
            data['receive_newsletter'] if 'receive_newsletter' in data.keys() else profile.receive_newsletter
        profile.save()

    def deactivate_user(self):
        self.is_active = False
        self.save()
        return self

    def generate_key(self, key_type):
        import random
        result = "".join([random.choice("0123456789") for i in range(4)])
        if key_type == 'phone':
            self.phone_change_key = result
        elif key_type == 'password':
            self.password_reset_key = result
        else:
            pass
        self.save()

    def get_cart(self):
        if self.is_authenticated and self.is_buyer and self.profile and self.profile.cart:
            return self.profile.cart
        return None

    def get_buyer_username(self):
        return self.username.split('_site_')[0]

    @staticmethod
    def create_buyer_username(username, shop_id):
        return f"{username}_shop_{shop_id}"

    def role(self):
        if self.is_buyer and hasattr(self, 'profile'):
            return self.profile.get_role_display()
        if not self.is_buyer and not self.is_shop_buyer and hasattr(self, 'manager'):
            return self.manager.get_role_display()
        if self.is_shop_buyer:
            from shop.models import Shop
            shop_id = self.username.split('_shop_')[-1]
            shop_title = Shop.objects.filter(id=shop_id).first().title
            return f'Покупатель магазина "{shop_title}"'
        return '-'
    role.short_description = "Роль пользователя"

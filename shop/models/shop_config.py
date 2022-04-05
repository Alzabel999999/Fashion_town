from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from garpix_utils.file_field import get_file_path
from ..models import Shop
from garpix_order.models import Country


class ShopConfig(models.Model):

    shop = models.OneToOneField(Shop, verbose_name='Магазин', on_delete=models.CASCADE,
                                related_name='shop_config', blank=False, null=False, default=None)

    main_first_background = models.FileField(upload_to=get_file_path, default='', blank=True,
                                             verbose_name='Фон на первом экране')
    main_first_text = RichTextUploadingField(verbose_name='Текст на первом экране', blank=True, default='')
    main_banner_1 = models.FileField(upload_to=get_file_path, default='', blank=True, verbose_name='Баннер 1')
    main_banner_2 = models.FileField(upload_to=get_file_path, default='', blank=True, verbose_name='Баннер 2')
    main_banner_3 = models.FileField(upload_to=get_file_path, default='', blank=True, verbose_name='Баннер 3')

    info_delivery = RichTextUploadingField(verbose_name='Информация о доставке', blank=True, default='')
    info_delivery_photo = models.FileField(verbose_name='Информация о доставке (фото)',
                                           upload_to=get_file_path, blank=True, default='')
    info_payment = RichTextUploadingField(verbose_name='Информация об оплате', blank=True, default='')
    info_payment_photo = models.FileField(verbose_name='Информация об оплате (фото)',
                                          upload_to=get_file_path, blank=True, default='')
    info_exchange = RichTextUploadingField(verbose_name='Информация о возврате и обмене', blank=True, default='')
    info_exchange_photo = models.FileField(verbose_name='Информация о возврате и обмене (фото)',
                                           upload_to=get_file_path, blank=True, default='')
    info_juridical = RichTextUploadingField(verbose_name='Юридическая информация', blank=True, default='')
    info_juridical_photo = models.FileField(verbose_name='Юридическая информация (фото)',
                                            upload_to=get_file_path, blank=True, default='')

    about_logo = models.FileField(upload_to=get_file_path, default='', blank=True, verbose_name='Лого')
    about_photo = models.FileField(upload_to=get_file_path, default='', blank=True, verbose_name='Фото')
    about_short_description = RichTextUploadingField(verbose_name='Краткий текст о компании', blank=True, default='')
    about_full_description = RichTextUploadingField(verbose_name='Полный текст о компании', blank=True, default='')

    contacts_title = models.CharField(verbose_name='Название магазина', max_length=256, default='')
    contacts_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    contacts_email = models.EmailField(verbose_name='Email', blank=True)
    contacts_country = models.ForeignKey(Country, verbose_name='Страна', related_name='country_contacts_countries',
                                         on_delete=models.SET_NULL, default=None, blank=True, null=True)
    contacts_city = models.CharField(max_length=256, blank=True, null=True, verbose_name='Город, район')
    contacts_street = models.CharField(max_length=512, blank=True, null=True,
                                       verbose_name='Название улицы, номер дома, корпус, строение, номер квартиры')
    contacts_domofon = models.CharField(max_length=256, blank=True, null=True, verbose_name='Этаж, домофон и т.д.')
    contacts_post_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Почтовый индекс')
    contacts_social_vk = models.CharField(max_length=512, blank=True, null=True, verbose_name='VK')
    contacts_social_insta = models.CharField(max_length=512, blank=True, null=True, verbose_name='Instagram')
    contacts_social_fb = models.CharField(max_length=512, blank=True, null=True, verbose_name='Facebook')
    contacts_text = models.TextField(blank=True, null=True, verbose_name='Краткий текст')

    footer_logo = models.FileField(upload_to=get_file_path, default='', blank=True, verbose_name='Лого')
    footer_policy = models.FileField(upload_to=get_file_path, default='', blank=True,
                                     verbose_name='Политика конфиденциальности')
    footer_country = models.ForeignKey(Country, verbose_name='Страна', related_name='country_footer_countries',
                                         on_delete=models.SET_NULL, default=None, blank=True, null=True)
    footer_city = models.CharField(max_length=256, blank=True, null=True, verbose_name='Город, район')
    footer_street = models.CharField(max_length=512, blank=True, null=True,
                                       verbose_name='Название улицы, номер дома, корпус, строение, номер квартиры')
    footer_domofon = models.CharField(max_length=256, blank=True, null=True, verbose_name='Этаж, домофон и т.д.')
    footer_post_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Почтовый индекс')
    footer_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    footer_email = models.EmailField(verbose_name='Email', blank=True)
    footer_social_vk = models.CharField(max_length=512, blank=True, null=True, verbose_name='VK')
    footer_social_insta = models.CharField(max_length=512, blank=True, null=True, verbose_name='Instagram')
    footer_social_fb = models.CharField(max_length=512, blank=True, null=True, verbose_name='Facebook')

    delivery_method_1_title = models.CharField(max_length=256, blank=True, null=True,
                                               verbose_name='Метод доставки 1')
    delivery_method_1_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                                  verbose_name='Цена доставки 1')
    delivery_method_2_title = models.CharField(max_length=256, blank=True, null=True,
                                               verbose_name='Метод доставки 2')
    delivery_method_2_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                                  verbose_name='Цена доставки 2')
    delivery_method_3_title = models.CharField(max_length=256, blank=True, null=True,
                                               verbose_name='Метод доставки 3')
    delivery_method_3_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                                  verbose_name='Цена доставки 3')

    class Meta:
        verbose_name = 'Конфигурация магазина'
        verbose_name_plural = 'Конфигурации магазинов'

    def __str__(self):
        return f'Конфигурация магазина {self.shop.title}'

    def update_double(self, data):
        print(data)
        if 'contacts_phone' in data.keys():
            self.contacts_phone = data['contacts_phone']
            self.footer_phone = data['contacts_phone']
        if 'contacts_email' in data.keys():
            self.contacts_email = data['contacts_email']
            self.footer_email = data['contacts_email']
        if 'contacts_country' in data.keys():
            self.contacts_country = data['contacts_country']
            self.footer_country = data['contacts_country']
        if 'contacts_city' in data.keys():
            self.contacts_city = data['contacts_city']
            self.footer_city = data['contacts_city']
        if 'contacts_street' in data.keys():
            self.contacts_street = data['contacts_street']
            self.footer_street = data['contacts_street']
        if 'contacts_domofon' in data.keys():
            self.contacts_domofon = data['contacts_domofon']
            self.footer_domofon = data['contacts_domofon']
        if 'contacts_post_code' in data.keys():
            self.contacts_post_code = data['contacts_post_code']
            self.footer_post_code = data['contacts_post_code']
        if 'contacts_social_vk' in data.keys():
            self.contacts_social_vk = data['contacts_social_vk']
            self.footer_social_vk = data['contacts_social_vk']
        if 'contacts_social_insta' in data.keys():
            self.contacts_social_insta = data['contacts_social_insta']
            self.footer_social_insta = data['contacts_social_insta']
        if 'contacts_social_fb' in data.keys():
            self.contacts_social_fb = data['contacts_social_fb']
            self.footer_social_fb = data['contacts_social_fb']
        if 'footer_phone' in data.keys():
            self.footer_phone = data['footer_phone']
            self.contacts_phone = data['footer_phone']
        if 'footer_email' in data.keys():
            self.footer_email = data['footer_email']
            self.contacts_email = data['footer_email']
        if 'footer_country' in data.keys():
            self.footer_country = data['footer_country']
            self.contacts_country = data['footer_country']
        if 'footer_city' in data.keys():
            self.footer_city = data['footer_city']
            self.contacts_city = data['footer_city']
        if 'footer_street' in data.keys():
            self.footer_street = data['footer_street']
            self.contacts_street = data['footer_street']
        if 'footer_domofon' in data.keys():
            self.footer_domofon = data['footer_domofon']
            self.contacts_domofon = data['footer_domofon']
        if 'footer_post_code' in data.keys():
            self.footer_post_code = data['footer_post_code']
            self.contacts_post_code = data['footer_post_code']
        if 'footer_social_vk' in data.keys():
            self.footer_social_vk = data['footer_social_vk']
            self.contacts_social_vk = data['footer_social_vk']
        if 'footer_social_insta' in data.keys():
            self.footer_social_insta = data['footer_social_insta']
            self.contacts_social_insta = data['footer_social_insta']
        if 'footer_social_fb' in data.keys():
            self.footer_social_fb = data['footer_social_fb']
            self.contacts_social_fb = data['footer_social_fb']
        self.save()
        return True

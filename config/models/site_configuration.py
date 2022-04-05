from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from garpix_page.models import Page
from garpix_utils.file_field import get_file_path
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    vk_link = models.CharField(max_length=512, blank=True, default='https://paste_link/',
                               verbose_name='Ссылка вКонтакте')
    insta_link = models.CharField(max_length=512, blank=True, default='https://paste_link/',
                                  verbose_name='Ссылка Instagram')
    fb_link = models.CharField(max_length=512, blank=True, default='https://paste_link/',
                               verbose_name='Ссылка Facebook')
    whatsapp_link = models.CharField(max_length=512, blank=True, default='https://paste_link/',
                                     verbose_name='Ссылка WhatsApp')
    telegram_link = models.CharField(max_length=512, blank=True, default='https://paste_link/',
                                     verbose_name='Ссылка Telegram')
    viber_link = models.CharField(max_length=512, blank=True, default='https://paste_link/',
                                  verbose_name='Ссылка Viber')

    logo_1 = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True, verbose_name='Лого шапки сайта')
    logo_2 = models.FileField(
        max_length=255, upload_to=get_file_path, default='', blank=True, verbose_name='Лого подвала сайта')
    logo_text = models.TextField(blank=True, verbose_name='Текст рядом с лого',
                                 default='')
    policy = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True,
                              verbose_name='Политика конфиденциальности')
    terms = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True,
                             verbose_name='Пользовательское соглашение')
    order_condition = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True,
                                       verbose_name='Условия оформления заказа')
    return_rules = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True,
                                    verbose_name='Правила возврата')

    contacts = RichTextUploadingField(blank=True, verbose_name='Контакты', default='')

    page_type_landing = models.ForeignKey(Page, verbose_name='Страница лендинга', blank=True, null=True,
                                          limit_choices_to={'page_type': settings.PAGE_TYPE_LANDING},
                                          on_delete=models.SET_NULL, related_name='conf_landing')
    page_type_cart = models.ForeignKey(Page, verbose_name='Страница корзины', blank=True, null=True,
                                       limit_choices_to={'page_type': settings.PAGE_TYPE_CART},
                                       on_delete=models.SET_NULL, related_name='conf_cart')
    page_type_account = models.ForeignKey(Page, verbose_name='Страница ЛК', blank=True, null=True,
                                          limit_choices_to={'page_type': settings.PAGE_TYPE_ACCOUNT},
                                          on_delete=models.SET_NULL, related_name='conf_account')
    page_type_profile = models.ForeignKey(Page, verbose_name='Страница профиля', blank=True, null=True,
                                          limit_choices_to={'page_type': settings.PAGE_TYPE_PROFILE},
                                          on_delete=models.SET_NULL, related_name='conf_profile')
    page_type_auth = models.ForeignKey(Page, verbose_name='Страница авторизации', blank=True, null=True,
                                       limit_choices_to={'page_type': settings.PAGE_TYPE_AUTH},
                                       on_delete=models.SET_NULL, related_name='conf_auth')
    page_type_reg = models.ForeignKey(Page, verbose_name='Страница регистрации', blank=True, null=True,
                                      limit_choices_to={'page_type': settings.PAGE_TYPE_REGISTRATION},
                                      on_delete=models.SET_NULL, related_name='conf_reg')
    page_type_reset_pass = models.ForeignKey(Page, verbose_name='Страница Вспомнить пароль', blank=True, null=True,
                                             limit_choices_to={'page_type': settings.PAGE_TYPE_RESET_PASS},
                                             on_delete=models.SET_NULL, related_name='conf_reset_pass')
    page_type_checkout = models.ForeignKey(Page, verbose_name='Страница оформления заказа', blank=True, null=True,
                                           limit_choices_to={'page_type': settings.PAGE_TYPE_CHECKOUT},
                                           on_delete=models.SET_NULL, related_name='conf_checkout')
    page_type_order_history = models.ForeignKey(Page, verbose_name='Страница история заказов', blank=True, null=True,
                                                limit_choices_to={'page_type': settings.PAGE_TYPE_ORDER_HISTORY},
                                                on_delete=models.SET_NULL, related_name='conf_order_history')
    page_type_wishlist = models.ForeignKey(Page, verbose_name='Страница Избранное (вишлист)', blank=True, null=True,
                                           limit_choices_to={'page_type': settings.PAGE_TYPE_WISHLIST},
                                           on_delete=models.SET_NULL, related_name='conf_wishlist')
    page_type_comparsion = models.ForeignKey(Page, verbose_name='Страница Сравнить', blank=True, null=True,
                                             limit_choices_to={'page_type': settings.PAGE_TYPE_COMPARSION},
                                             on_delete=models.SET_NULL, related_name='conf_comparsion')
    page_type_search = models.ForeignKey(Page, verbose_name='Страница Поиск', blank=True, null=True,
                                         limit_choices_to={'page_type': settings.PAGE_TYPE_SEARCH},
                                         on_delete=models.SET_NULL, related_name='conf_search')
    page_type_catalog = models.ForeignKey(Page, verbose_name='Страница Каталог', blank=True, null=True,
                                          limit_choices_to={'page_type': settings.PAGE_TYPE_CATALOG},
                                          on_delete=models.SET_NULL, related_name='conf_catalog')
    page_type_news = models.ForeignKey(Page, verbose_name='Страница Новости', blank=True, null=True,
                                       limit_choices_to={'page_type': settings.PAGE_TYPE_NEWS},
                                       on_delete=models.SET_NULL, related_name='conf_news')
    page_type_reviews = models.ForeignKey(Page, verbose_name='Страница Отзывы', blank=True, null=True,
                                          limit_choices_to={'page_type': settings.PAGE_TYPE_INFO_REVIEWS},
                                          on_delete=models.SET_NULL, related_name='conf_reviews')
    page_type_live_photos = models.ForeignKey(Page, verbose_name='Страница Живые фото', blank=True, null=True,
                                              limit_choices_to={'page_type': settings.PAGE_TYPE_LIVE_PHOTOS},
                                              on_delete=models.SET_NULL, related_name='conf_live_photos')
    page_type_shop_create = models.ForeignKey(Page, verbose_name='Страница создания ИМ', blank=True, null=True,
                                              limit_choices_to={'page_type': settings.PAGE_TYPE_SHOP_CREATE},
                                              on_delete=models.SET_NULL, related_name='conf_shop_create')
    page_type_404 = models.ForeignKey(Page, verbose_name='Страница 404', blank=True, null=True,
                                      limit_choices_to={'page_type': settings.PAGE_TYPE_404},
                                      on_delete=models.SET_NULL, related_name='conf_404')
    page_type_500 = models.ForeignKey(Page, verbose_name='Страница 500', blank=True, null=True,
                                      limit_choices_to={'page_type': settings.PAGE_TYPE_500},
                                      on_delete=models.SET_NULL, related_name='conf_500')

    robots_txt = models.TextField(blank=True, verbose_name='robots.txt content', default='')
    scripts = models.TextField(blank=True, verbose_name='metric scripts', default='')

    def __str__(self):
        return 'Настройки сайта'

    class Meta:
        verbose_name = 'Настройки сайта'

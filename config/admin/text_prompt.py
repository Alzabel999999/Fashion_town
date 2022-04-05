from django.contrib import admin
from solo.admin import SingletonModelAdmin
from ..models import TextPrompt


@admin.register(TextPrompt)
class TextPromptAdmin(SingletonModelAdmin):
    pass
    # fieldsets = (
    #     ('Оформление', {'fields': (
    #         'logo_1', 'logo_2', 'logo_text', 'policy', 'terms', 'order_condition', 'return_rules')}),
    #     ('Соцсети', {'fields': ('vk_link', 'insta_link', 'fb_link')}),
    #     ('Разное', {'fields': ('contacts',)}),
    #     ('Страницы', {'fields': (
    #         'page_type_cart', 'page_type_account', 'page_type_auth', 'page_type_reg', 'page_type_reset_pass',
    #         'page_type_checkout', 'page_type_order_history', 'page_type_wishlist', 'page_type_comparsion',
    #         'page_type_search', 'page_type_catalog', 'page_type_news', 'page_type_reviews', 'page_type_landing',
    #         'page_type_live_photos', 'page_type_shop_create', 'page_type_404', 'page_type_500')}),
    #     ('Роботы', {'fields': ('robots_txt', 'scripts')}),
    # )

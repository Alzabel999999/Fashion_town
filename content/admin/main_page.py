from django.contrib import admin
from solo.admin import SingletonModelAdmin
from ..models.main_page import MainPage


@admin.register(MainPage)
class MainPageAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Первый экран', {'fields': ('title', 'overtitle', 'undertitle', 'filters', 'image')}),
        ('Товары "в наличии"', {'fields': ('in_stock_product_filters', )}))

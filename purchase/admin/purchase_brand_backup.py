from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render
from django.urls import path
from ..models import PurchaseBrand
from garpix_catalog.models import Brand
from garpix_order.models import OrderItem
from ..serializers import ProductSerializer


@admin.register(PurchaseBrand)
class PurchaseBrandAdmin(admin.ModelAdmin):

    list_display = ['title', 'condition', 'ordered_in_brand', 'producer']
    search_fields = ['title', ]
    change_form_template = 'admin/purchase_brand.html'

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser or user.groups.filter(name__icontains='админ').exists():
            order_items = OrderItem.objects.all().order_by('-order__id', 'product__id').distinct('order', 'product')
        elif user.groups.filter(name__icontains='закуп').exists():
            order_items = OrderItem.objects.filter(
                status__in=['paid', 'ordered', 'redeemed', 'replacement']).order_by(
                '-order__id', 'product__id').distinct('order', 'product')
        else:
            order_items = OrderItem.objects.none()
        return Brand.objects.filter(
            Q(brand_products__product_cart_packs__cart_items_pack_order_items__in=order_items) |
            Q(brand_products__product_skus__sku_cart_items__cart_item_order_items__in=order_items)
        ).distinct()

    def delete_queryset(self, request, queryset):
        pass

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:pk>/change/', self.purchase_brand),
            path('<int:pk>/change/set_order_item_status/', self.set_order_item_status, name='set_order_item_status'),
        ]
        return my_urls + urls

    def purchase_brand(self, request, pk):
        status = request.GET.get('status', 'all')
        brand = self.get_object(request, pk)
        order_items = OrderItem.objects.all() if status == 'all' else OrderItem.objects.filter(status=status)
        products = order_items.filter(product__product__brand=brand).order_by('-order__id', 'product__id')
        statuses = [{
            'value': status_item[0],
            'label': status_item[1],
            'active': status == status_item[0]
        } for status_item in settings.CHOICE_ORDER_ITEM_STATUSES]
        filter_statuses = statuses.copy()
        filter_statuses.append({'value': 'all', 'label': 'Все статусы', 'active': status == 'all'})
        context = {
            'filter_statuses': filter_statuses,
            'item_statuses': statuses,
            'brand': {
                'title': brand.title,
                'condition': brand.brand_rc,
                'ordered_in_brand': products.count(),
            },
            'site_url': settings.SITE_URL,
            'purchase_order_url': settings.SITE_URL + '/admin/purchase/purchaseorder/',
            'products': ProductSerializer(products.distinct('order', 'product'), many=True).data,
        }
        return render(request, template_name='admin/purchase_brand.html', context=context)

    def set_order_item_status(self, request, pk):
        if request.method == 'POST' and '_set_order_item_status' in request.POST.keys():
            item_id = request.POST.get('item_id', None)
            if item_id:
                order_item = OrderItem.objects.filter(id=item_id).first()
                same_order_items = order_item.get_same_order_items()
                status = request.POST.get('status', None)
                if status and order_item:
                    same_order_items.update(status=status)
                    self.message_user(request,
                                      f"статус товара успешно изменен на \"{order_item.get_status_display()}\"",
                                      level=messages.DEFAULT_LEVELS['INFO'])
                    if status == 'redeemed':
                        if order_item.order.order_items.filter(status='redeemed').count()\
                                == order_item.order.order_items.all().count():
                            order_item.order.status = 'redeemed'
                            order_item.order.save()
                            self.message_user(request, "все товары заказа выкуплены... заказ выкуплен",
                                              level=messages.DEFAULT_LEVELS['INFO'])
                else:
                    self.message_user(request, f"wrong status", level=messages.DEFAULT_LEVELS['ERROR'])
            else:
                self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
            return HttpResponseRedirect("../")
        self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")

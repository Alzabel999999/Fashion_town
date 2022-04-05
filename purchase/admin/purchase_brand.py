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
from django.http import HttpResponse
from django.db.models import Count
from django.http import HttpResponse

@admin.register(PurchaseBrand)
class PurchaseBrandAdmin(admin.ModelAdmin):

    list_display = ['title', 'condition', 'ordered_in_brand', 'producer']
    search_fields = ['title', ]
    change_form_template = 'admin/purchase_brand.html'

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser or user.groups.filter(name__icontains='админ').exists():
            order_items = OrderItem.objects.all().order_by('product__id').distinct('product')
        elif user.groups.filter(name__icontains='закуп').exists():
            order_items = OrderItem.objects.filter(
                status__in=['paid', 'ordered', 'redeemed', 'replacement']).order_by('product__id').distinct('product')
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
        statuses = request.GET.getlist('status')
        if statuses != []:
            statuses = statuses
        else:
            statuses = ['all']

        brand = self.get_object(request, pk)
        #order_items = OrderItem.objects.all() if status == 'all' else OrderItem.objects.filter(status=status)
        order_items = OrderItem.objects.all()
        order_items = order_items.filter(status__in=statuses)

        if statuses[0] == 'all':
            order_items = OrderItem.objects.all()
        products = order_items.filter(product__product__brand=brand).exclude(status='canceled').order_by('product__id')#.exclude(status='canceled').

        statuses = [{
            'value': status_item[0],
            'label': status_item[1],
            'active': status == status_item[0]
        } for status_item in settings.CHOICE_ORDER_ITEM_STATUSES]
        filter_statuses = statuses.copy()
        for status in filter_statuses:
            if status['value'] == 'canceled':
                del filter_statuses[filter_statuses.index(status)]
                break
        filter_statuses.append({'value': 'all', 'label': 'Все статусы', 'active': status == 'all'})

        context = {
            'site_url': settings.SITE_URL,
            'filter_statuses': filter_statuses,
            'item_statuses': statuses,
            'brand': {
                'title': brand.title,
                'condition': brand.brand_rc,
                'ordered_in_brand': len(products),
            },
            'site_url': settings.SITE_URL,
            'purchase_order_url': settings.SITE_URL + '/admin/purchase/purchaseorder/',
            'products': ProductSerializer(products.distinct('product', 'status'), many=True).data, #ProductSerializer(products.distinct('product').order_by('status').distinct('status'), many=True).data
        }
        #return HttpResponse(products)
        return render(request, template_name='admin/purchase_brand.html', context=context)

    def set_order_item_status(self, request, pk):
        if request.method == 'POST' and '_set_order_item_status' in request.POST.keys():
            item_id = request.POST.get('item_id', None)
            amount = request.POST.get('amount', None)

            if item_id:
                status = request.POST.get('status', None)
                if str(status) == 'payment_waiting':
                    status_show = 'Ожидается оплата'
                if str(status) == 'paid':
                    status_show = 'Товар оплачен'
                if str(status) == 'ordered':
                    status_show = 'Товар заказан'
                if str(status) == 'redeemed':
                    status_show = 'Товар выкуплен'
                if str(status) == 'packaging':
                    status_show = 'Товар на упаковке'
                if str(status) == 'sended':
                    status_show = 'Товар отправлен'
                if str(status) == 'replacement':
                    status_show = 'Замена товара'
                if str(status) == 'canceled':
                    status_show = 'Отмена товара'
                if str(status) == 'collection':
                    status_show = 'В сборе'
                #old_status = request.POST.get('old_status', None)
                #self.message_user(request, str(status), level=messages.DEFAULT_LEVELS['INFO'])
                #self.message_user(request, str(status), level=messages.DEFAULT_LEVELS['INFO'])
                order_item = OrderItem.objects.filter(id=item_id).first()
                old_status = order_item.status
                #self.message_user(request, str(old_status), level=messages.DEFAULT_LEVELS['INFO'])
                try:
                    same_order_items = OrderItem.objects.filter(product=order_item.product,status=old_status)[:int(amount)]
                except:
                    self.message_user(request,
                                      f"ВЫ НЕ ВВЕЛИ КОЛИЧЕСТВО ТОВАРА ДЛЯ ИЗМЕНЕНИЯ", #order_item.get_status_display()
                                      level=messages.DEFAULT_LEVELS['INFO'])
                    return HttpResponseRedirect("../")
                #same_order_items = order_item.get_same_order_items()
                #self.message_user(request, str(same_order_items), level=messages.DEFAULT_LEVELS['INFO'])
                if status and order_item:
                    for tt in same_order_items:
                        #tt.update(status=status)
                        #self.message_user(request, str(tt.status), level=messages.DEFAULT_LEVELS['INFO'])
                        tt.status = str(status)
                        tt.save()
                        #self.message_user(request, str(tt.status), level=messages.DEFAULT_LEVELS['INFO'])
                    #same_order_items.update(status=status)
                    #OrderItem.objects.filter(pk__in=list(same_order_items)).update(status=status)
                    self.message_user(request,
                                      f"статус товара успешно изменен на \"{status_show}\"", #order_item.get_status_display()
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

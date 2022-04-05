from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import path
from django.db.models import Q, Count
from django.template import Template, Context
from ..models import PurchaseOrder
from garpix_order.models import Order
from ..serializers import ProductSerializer
import os
from garpix_utils.file_field import get_file_path
from garpix_utils.htmltopdf import str_to_pdf
from datetime import datetime
from django.contrib.admin import SimpleListFilter
from user.models import Notification

class PurchaseOrderFilter(SimpleListFilter):
    title = 'Статусы' # or use _('country') for translated title
    parameter_name = 'purchase_order'

    def lookups(self, request, model_admin):
        user = request.user
        if user.groups.filter(Q(name__icontains='склад') | Q(name__icontains='упак')).exists():
            settings_choises = [('redeemed', 'Заказ выкуплен'), ('packaging', 'Упаковка заказа'), ('delivery_payment_waiting', 'Ожидается оплата за доставку'), ('sended', 'Заказ отправлен')]
        else:
            settings_choises = settings.CHOICE_ORDER_STATUSES

        countries = set([c for c in settings_choises])#settings.CHOICE_ORDER_STATUSES])
        return [(c) for c in countries]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        else:
            return queryset


@admin.register(PurchaseOrder)#Purchase

class PurchaseOrderAdmin(admin.ModelAdmin):
    #fieldsets = (
        #(None, {'fields': ('order_number', 'items_count', 'status')}),)
    list_display = ['order_number', 'items_count', 'status']
    change_form_template = 'admin/purchase_order.html'
    #fields = ['order_number', 'items_count', 'status']
    #def status(self):
        #return self.purchase_order
    #list_filter = (('status', admin.RelatedOnlyFieldListFilter))
    list_filter = (PurchaseOrderFilter,)

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser or user.groups.filter(name__icontains='админ').exists():
            return Order.objects.annotate(order_items_count=Count('order_items')).filter(order_items_count__gt=0)
        elif user.groups.filter(Q(name__icontains='склад') | Q(name__icontains='упак')).exists():
            return Order.objects.filter(
                status__in=['redeemed', 'packaging', 'delivery_payment_waiting', 'sended']).annotate(
                order_items_count=Count('order_items')).filter(order_items_count__gt=0)
        return Order.objects.none()

    def delete_queryset(self, request, queryset):
        pass

    #def get_status(self, request):
        #return request.status

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:pk>/change/', self.purchase_order),
            path('<int:pk>/change/set_track_number/', self.set_track_number, name='set_track_number'),
            path('<int:pk>/change/set_delivery_cost/', self.set_delivery_cost, name='set_delivery_cost'),
            path('<int:pk>/change/set_delivery_weight/', self.set_delivery_weight, name='set_delivery_weight'),
            path('<int:pk>/change/set_order_status/', self.set_order_status, name='set_order_status'),
            path('<int:pk>/change/confirm_delivery_payment/', self.confirm_delivery_payment,
                 name='confirm_delivery_payment'),
            path('<int:pk>/change/get_order_specification/', self.get_order_specification,
                 name='get_order_specification'),
        ]
        return my_urls + urls

    def get_context(self, request, pk):
        order = self.get_object(request, pk)
        products = order.order_items.all().order_by('product__id')#.distinct('product')
        count = len(order.order_items.all())
        statuses = [{
            'value': status_item[0],
            'label': status_item[1],
            'active': order.status == status_item[0]
        } for status_item in settings.CHOICE_ORDER_STATUSES]
        #self.message_user(request, settings.CHOICE_ORDER_STATUSES, level=messages.DEFAULT_LEVELS['ERROR'])
        context = {
            'statuses': statuses,
            'count': count,
            'order': {
                'number': order.order_number,
                'delivery': {
                    'cost': order.order_delivery.cost if hasattr(order, 'order_delivery') else '0.00',
                    'status': order.order_delivery.status if hasattr(order, 'order_delivery') else '',
                },
                'buyer_role': order.profile.role,
                'delivery_method': order.delivery_method,
                'delivery_address': order.delivery_address,
                'weight': order.weight,
            },
            'site_url': settings.SITE_URL,
            'products': ProductSerializer(products, many=True).data,
            'track_number': order.track_number,
            'specification': settings.SITE_URL + order.specification.url if order.specification else '#'
        }
        return context

    def purchase_order(self, request, pk):
        context = self.get_context(request, pk)
        return render(request, template_name='admin/purchase_order.html', context=context)

    def set_track_number(self, request, pk):
        if request.method == 'POST' and '_set_track_number' in request.POST.keys():
            order = self.get_object(request, pk)
            track_number = request.POST.get('track_number', '')
            order.track_number = track_number
            order.save()
            from user.models import Notification
            profile =order.profile

            order_url = settings.SITE_URL_FRONT + order.order_number
            url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
            notification = Notification(profile=profile, message='{0} трек-номер для отслеживания заказа № {1} '.format(track_number, url))
            notification.save()
            return HttpResponseRedirect("../")
        self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")

    def set_delivery_cost(self, request, pk):
        if request.method == 'POST' and '_set_delivery_cost' in request.POST.keys():
            order = self.get_object(request, pk)
            from decimal import Decimal
            try:
                delivery_cost = Decimal(request.POST.get('delivery_cost', 0))
            except:
                self.message_user(request, f"Введите правильно число", level=messages.DEFAULT_LEVELS['ERROR'])
                return HttpResponseRedirect("../")
            from garpix_order.models import Delivery
            Delivery.objects.get_or_create(order=order)
            order.order_delivery.cost = delivery_cost
            order.order_delivery.status = 'delivery_payment_waiting'
            order.order_delivery.save()
            order.status = settings.ORDER_STATUS_DELIVERY_PAYMENT_WAITING
            order.save()
            if order.profile.balance >= delivery_cost:
                order.profile.balance -= delivery_cost
                order.profile.save()
                #order.total_cost = order.total_cost + order.order_delivery.cost
                #                                                                               order.save()
                post_data = request.POST.copy()
                post_data.update({'_confirm_delivery_payment': ''})
                request.POST = post_data
                self.confirm_delivery_payment(request, pk)
            else:
                profile = order.profile
                notification = Notification(profile=profile, message='Вам нужно оплатить доставку товара {0} на сумму {1}'.format(order.id, delivery_cost))
                notification.save()
            return HttpResponseRedirect("../")
        self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")

    def set_delivery_weight(self, request, pk):
        if request.method == 'POST' and '_set_delivery_weight' in request.POST.keys():
            order = self.get_object(request, pk)
            from decimal import Decimal
            try:
                delivery_weight = Decimal(request.POST.get('delivery_weight', 0))
            except:
                self.message_user(request, f"Введите правильно число", level=messages.DEFAULT_LEVELS['ERROR'])
                return HttpResponseRedirect("../")

            order.weight = delivery_weight
            order.save()
            return HttpResponseRedirect("../")
        self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")

    def set_order_status(self, request, pk):
        if request.method == 'POST' and '_set_order_status' in request.POST.keys():
            order = self.get_object(request, pk)
            status = request.POST.get('status', None)
            if status:
                order.status = status
                order.save()
                from user.models import Notification
                if order.status != order.old_status:
                    order_url = settings.SITE_URL_FRONT + order.order_number
                    url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
                    notification = Notification(profile=order.profile, message='Статус Вашего заказа № {0} изменен на {1} '.format(url, settings.ORDER_STATUSES[order.status]['title']))
                    notification.save()
                    order.old_status = order.status
                    order.save()
                self.message_user(request, f"статус заказа успешно изменен на \"{order.get_status_display()}\"",
                                  level=messages.DEFAULT_LEVELS['INFO'])
                if status in ['packaging', 'sended', 'canceled']:
                    order.order_items.exclude(status='canceled').update(status=status)
                    self.message_user(request, f"всем товарам заказа присвоен статус"
                                               f" \"{settings.ORDER_ITEM_STATUSES[status]['title']}\"",
                                      level=messages.DEFAULT_LEVELS['INFO'])
            else:
                self.message_user(request, f"wrong status", level=messages.DEFAULT_LEVELS['ERROR'])
            return HttpResponseRedirect("../")
        self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")

    def confirm_delivery_payment(self, request, pk):
        if request.method == 'POST' and '_confirm_delivery_payment' in request.POST.keys():
            order = self.get_object(request, pk)
            order.order_delivery.status = 'delivery_payment_confirmed'
            order.order_delivery.save()
            order.status = settings.ORDER_STATUS_DELIVERY_PAID#settings.ORDER_STATUS_SENDED
            order.save()
            return HttpResponseRedirect("../")
        self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")

    def get_order_specification(self, request, pk):
        if '_get_order_specification' in request.POST.keys():
            context = self.get_context(request, pk)
            order = self.get_object(request, pk)
            now = datetime.now()
            context['now'] = now
            now_str = now.strftime('%Y%m%d%H%M%S')
            doc_name = f'спецификация заказа №{order.order_number} от {now_str}'
            pdf = self.generate_pdf_file(context=context, doc_name=doc_name)
            order.specification = pdf
            order.save()
            return HttpResponseRedirect("../")
        self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")

    def generate_pdf_file(self, context, doc_name, options={}):
        with open(settings.BASE_DIR + '/purchase/templates/admin/specification.html', 'r') as f:
            template_str = f.read()
            f.close()
        template = Template(template_str)
        context = Context(dict_=context)
        html = template.render(context)
        path = os.path.join(get_file_path(None, f'{doc_name}.pdf'))
        options['load-error-handling'] = 'ignore'
        options['load-media-error-handling'] = 'ignore'
        str_to_pdf(html, os.path.join(settings.MEDIA_ROOT, path), options)
        return path

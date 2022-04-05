from django.db.models import Q
from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from ..models import PurchaseProduct
from garpix_order.models import OrderItem
from ..serializers import ProductCommentSerializer, PhotoSerializer, VideoSerializer, CorrespondenceSerializer, ProductSerializer, CorrespondenceOrderItemSerializer
from garpix_order.models import CorrespondenceItem, CorrespondenceOrderItem
from django.utils.safestring import mark_safe


@admin.register(PurchaseProduct)
class PurchaseProductAdmin(admin.ModelAdmin):

    list_display = ['purchase_title', 'purchase_size', 'purchase_color', 'purchase_product_brand', 'purchase_order', 'purchase_image']
    change_form_template = 'admin/purchase_product.html'

    def purchase_product_brand(self, request):
        return request.product.product.brand
    purchase_product_brand.short_description = 'Брэнд'
    def purchase_image(self, request):
        obj = request
        #order = ProductSerializer(obj, many=True).data
         #'http://91.218.229.240:8000/media/' +
        #return '<img src={0} />'.format(str(order))
        #return mark_safe('<img src={0} width="75" height="100" />'.format(url))
        try:
            url = str(request.product.get_image())
            return mark_safe('<a href="{0}" target="_blank"><img src="{0}" width="75" height="100"></a>'.format(url))
        except:
            return ''
    purchase_image.short_description = 'Превью'

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser or user.groups.filter(name__icontains='админ').exists():
            qs = OrderItem.objects.all().order_by('-order__id', 'product__id').distinct('order', 'product')
        elif user.groups.filter(name__icontains='закуп').exists():
            qs = OrderItem.objects.filter(
                status__in=['paid', 'ordered', 'redeemed', 'replacement']).order_by(
                '-order__id', 'product__id').distinct('order', 'product')
        elif user.groups.filter(Q(name__icontains='склад') | Q(name__icontains='упак')).exists():
            qs = OrderItem.objects.filter(
                status__in=['redeemed', 'packaging', 'sended']).order_by(
                '-order__id', 'product__id').distinct('order', 'product')
        else:
            qs = OrderItem.objects.none()
        qs = qs.exclude(status=settings.ORDER_ITEM_STATUS_CANCELED).exclude(order=None)
        return qs

    def delete_queryset(self, request, queryset):
        pass

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:pk>/change/', self.purchase_product),
            path('<int:pk>/change/create_message/', self.create_message, name='create_message'),
            path('<int:pk>/change/create_message_order_item/', self.create_message_order_item, name='create_message_order_item'),
        ]
        return my_urls + urls

    def get_context(self, request, pk):
        product = self.get_object(request, pk)
        count_total = OrderItem.objects.filter(product=product.product).count()
        count_in_order = OrderItem.objects.filter(product=product.product, order=product.order).count()
        try:
            #comment = OrderItem.objects.filter(product=product.product, order=product.order).first()
            comment = product




        except:
            comment = '-'
        #item_id = OrderItem.objects.filter(product=product.product, order=product.order).first().id
        item_id = product.id
        try:
            order_comment = product.order.comment
        except:
            order_comment = ''
        correspondence = product.order.correspondence_messages.all().order_by('-created_at')
        #order_item_correspondence = OrderItem.objects.filter(product=product.product, order=product.order).first().correspondence_messages.all().order_by('-created_at')
        order_item_correspondence = product.correspondence_messages.all().order_by('-created_at')
        context = {
            'id': product.product.id,
            'title': product.title,
            'color': product.product.color,
            'size': product.product.size,
            'brand': product.product.product.brand,
            'brand_url': settings.SITE_URL + f'/admin/purchase/purchasebrand/{product.product.product.brand.id}/change/',
            'category': product.product.product.category,
            'order': product.order.order_number,
            'order_url': settings.SITE_URL + f'/admin/purchase/purchaseorder/{product.order.id}/change/',
            'condition': product.product.product.get_condition(),
            'count_total': count_total,
            'count_in_order': count_in_order,
            'videos': VideoSerializer(product.product.product_sku_videos.all(), many=True).data,
            'photos': PhotoSerializer(product.product.product_sku_images.all(), many=True).data,
            'product_comment': ProductCommentSerializer(comment).data,
            'order_comment': order_comment,#CorrespondenceOrderItemSerializer(order_item_correspondence, many=True).data,
            'correspondence': CorrespondenceSerializer(correspondence, many=True).data,
            'correspondence_order_item': CorrespondenceOrderItemSerializer(order_item_correspondence, many=True).data,
            'item_id': item_id
        }
        return context

    def purchase_product(self, request, pk):
        context = self.get_context(request, pk)
        return render(request, template_name='admin/purchase_product.html', context=context)

    def create_message(self, request, pk):
        if request.method == 'POST' and '_create_message' in request.POST.keys():
            from user.models import Notification
            message = request.POST.get('message', '')
            product = self.get_object(request, pk)
            data = {'order': product.order.id, 'message': message}
            files = request.FILES.getlist('files', [])
            user = request.user
            CorrespondenceItem.create(user=user, data=data, files=files)
            profile = product.order.profile

            order_url = settings.SITE_URL_FRONT + product.order.order_number
            url = '<a href="{0}">{1}</a>'.format(order_url, product.order.order_number)
            notification = Notification(profile=profile, message='В заказе №{0} появился новый комментарий'.format(url))
            notification.save()
            return HttpResponseRedirect("../")
        self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")

    def create_message_order_item(self, request, pk):
        if request.method == 'POST' and '_create_message_order_item' in request.POST.keys():
            from user.models import Notification
            message = request.POST.get('message', '')
            item_id = request.POST.get('item_id', '')
            data = {'order_item_id': item_id, 'message': message}
            files = request.FILES.getlist('files', [])
            user = request.user
            order_item = OrderItem.objects.filter(id=item_id).first()
            CorrespondenceOrderItem.create(user=user, data=data, files=files)
            profile = order_item.order.profile

            order_url = settings.SITE_URL_FRONT + order_item.order.order_number
            url = '<a href="{0}">{1}</a>'.format(order_url, order_item.order.order_number)
            notification = Notification(profile=profile, message='В заказе №{0} появился новый комментарий'.format(url))
            notification.save()
            return HttpResponseRedirect("../")
        self.message_user(request, f"something wrong...", level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")

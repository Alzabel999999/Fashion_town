from django.conf import settings
from rest_framework import serializers
from garpix_order.models import OrderItem, CorrespondenceItem
from garpix_cart_rest.models import CartItemComment, CartItemCommentVideo, CartItemCommentPhoto
from ..mixins import ImageMixin, VideoMixin


class ProductSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    image_thumb = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    condition = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    order_number = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.title if obj.title else obj.product.product.title

    def get_image(self, obj):
        return obj.product.get_full_image()

    def get_image_thumb(self, obj):
        return obj.product.get_image()

    def get_price(self, obj):
        return obj.product.product.purchase_price

    def get_total_price(self, obj):
        price = obj.product.product.purchase_price
        count = OrderItem.objects.filter(order=obj.order, product=obj.product).count()
        return price * count

    def get_color(self, obj):
        return obj.product.color

    def get_size(self, obj):
        return obj.product.size

    def get_condition(self, obj):
        return obj.product.product.get_condition()

    def get_status(self, obj):
        #return obj.order.status
        return obj.get_status_display()

    def get_message(self, obj):
        if obj.order.correspondence_messages.all().exists():
            return 'Переписка'
        if obj.order.comment == '':
            return 'Комментарий к заказу'
        if obj.cart_item:
            if obj.cart_item.comment:
                return 'Комментарий к товару'
        if obj.cart_items_pack:
            if obj.cart_items_pack.comment:
                return 'Комментарий к товару'
        return '-'

    def get_order_number(self, obj):
        return obj.order.order_number

    def get_order_id(self, obj):
        return obj.order.id

    def get_count(self, obj):
        return OrderItem.objects.filter(product=obj.product, status=obj.order.status).count()
        #obj.order.status
        #return OrderItem.objects.filter(product=obj.product).count()

    def get_url(self, obj):
        return settings.SITE_URL + f'/admin/purchase/purchaseproduct/{obj.id}/change/'

    class Meta:
        model = OrderItem
        fields = [
            'id', 'title', 'image', 'image_thumb', 'price', 'total_price', 'color', 'size', 'condition', 'status',
            'message', 'order_number', 'order_id', 'count', 'url'
        ]


class ProductCommentSerializer(serializers.ModelSerializer):

    photos = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        return PhotoSerializer(obj.cart_item_comment_photos.all(), many=True).data

    def get_videos(self, obj):
        return VideoSerializer(obj.cart_item_comment_videos.all(), many=True).data

    class Meta:
        model = CartItemComment
        fields = ['comment', 'photos', 'videos']


class VideoSerializer(serializers.Serializer):

    video = serializers.SerializerMethodField()
    video_preview = serializers.SerializerMethodField()

    def get_video(self, obj):
        return settings.SITE_URL + obj.video.url

    def get_video_preview(self, obj):
        return settings.SITE_URL + obj.video_preview.url

    class Meta:
        model = VideoMixin
        fields = ['video', 'video_preview']


class PhotoSerializer(serializers.Serializer):

    image = serializers.SerializerMethodField()
    image_thumb = serializers.SerializerMethodField()

    def get_image(self, obj):
        return settings.SITE_URL + obj.image.url

    def get_image_thumb(self, obj):
        return settings.SITE_URL + obj.image_thumb

    class Meta:
        model = ImageMixin
        fields = ['image', 'image_thumb']


class CorrespondenceSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    def get_author(self, obj):
        # todo get author
        if obj.user.is_buyer:
            return 'Покупатель'
        elif hasattr(obj.user, 'manager'):
            return f'{obj.user.manager.get_role_display()} #{str(obj.user.manager.id)}'
        else:
            return '-'

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M:%S')

    def get_photos(self, obj):
        return PhotoSerializer(obj.correspondence_message_images.all(), many=True).data

    def get_videos(self, obj):
        return VideoSerializer(obj.correspondence_message_videos.all(), many=True).data

    class Meta:
        model = CorrespondenceItem
        fields = ['author', 'created_at', 'message', 'photos', 'videos']

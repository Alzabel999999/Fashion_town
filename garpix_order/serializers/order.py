from decimal import Decimal
from django.db.models import Sum, Q
from rest_framework import serializers
from .service import ServiceSerializer
from ..models import Order, OrderItem, CorrespondenceItem, CorrespondenceImage, CorrespondenceVideo, OrderItemCommentPhoto
from django.conf import settings
from garpix_cart_rest.models import Cart, CartItem, CartItemsPack
from garpix_catalog.models import Brand, Currency
from django.conf import settings


class OrderCorrespondenceImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_thumb = serializers.SerializerMethodField()

    def get_image(self, obj):
        return settings.SITE_URL + obj.image.url

    def get_image_thumb(self, obj):
        return settings.SITE_URL + obj.image_thumb

    class Meta:
        model = CorrespondenceImage
        fields = ['image', 'image_thumb']


class OrderCorrespondenceItemImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_thumb = serializers.SerializerMethodField()

    def get_image(self, obj):
        return settings.SITE_URL + obj.image.url

    def get_image_thumb(self, obj):
        return settings.SITE_URL + obj.image_thumb

    class Meta:
        model = CorrespondenceImage
        fields = ['image', 'image_thumb']


class OrderCorrespondenceVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()
    video_preview = serializers.SerializerMethodField()

    def get_video(self, obj):
        return settings.SITE_URL + obj.video.url

    def get_video_preview(self, obj):
        return settings.SITE_URL + obj.video_preview.url

    class Meta:
        model = CorrespondenceVideo
        fields = ['video', 'video_preview']


class OrderCorrespondenceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    is_me = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = self.context['request'].user
        return 'Вы' if user == obj.user else 'Менеджер'


    def get_images(self, obj):
        return OrderCorrespondenceImageSerializer(obj.correspondence_message_images.all(), many=True).data

    def get_videos(self, obj):
        return OrderCorrespondenceVideoSerializer(obj.correspondence_message_videos.all(), many=True).data

    def get_is_me(self, obj):
        user = self.context['request'].user
        return True if user == obj.user else False

    class Meta:
        model = CorrespondenceItem
        fields = ['user', 'message', 'images', 'videos', 'is_me', 'created_at']

class OrderCorrespondenceItemSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    is_me = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = self.context['request'].user
        return 'Вы' if user == obj.user else 'Менеджер'


    def get_images(self, obj):
        return OrderCorrespondenceItemImageSerializer(obj.correspondence_order_item_message_images.all(), many=True).data


    def get_is_me(self, obj):
        user = self.context['request'].user
        return True if user == obj.user else False

    class Meta:
        model = CorrespondenceItem
        fields = ['user', 'message', 'images', 'is_me', 'created_at']


class PassportMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'first_name', 'middle_name', 'last_name', 'passport_number', 'passport_issued', 'passport_issue_date']


class OrderItemSerializer(serializers.ModelSerializer):

    brand = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    change_agreement = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    comment_image = serializers.SerializerMethodField()

    def get_brand(self, obj):
        if obj.cart_item:
            return obj.cart_item.product.product.brand.title
        elif obj.cart_items_pack:
            return obj.cart_items_pack.product.brand.title
        else:
            return None

    def get_size(self, obj):
        if obj.cart_item:
            return obj.cart_item.product.size.get_size_name()
        elif obj.cart_items_pack:
            return obj.cart_items_pack.get_sizes()
        else:
            return None

    def get_color(self, obj):
        if obj.cart_item:
            return obj.cart_item.product.color.title
        elif obj.cart_items_pack:
            return obj.cart_items_pack.color.title
        else:
            return None

    def get_change_agreement(self, obj):
        if obj.cart_item:
            return obj.cart_item.change_agreement
        elif obj.cart_items_pack:
            return obj.cart_items_pack.change_agreement
        else:
            return None

    def get_comment(self, obj):
        # todo переделать под коммент из товара заказа
        if obj.comment:
            return obj.comment
        else:
            return ''
        """if obj.cart_item:
            return obj.cart_item.comment.comment if obj.cart_item.comment else ''
        elif obj.cart_items_pack:
            return obj.cart_items_pack.comment.comment if obj.cart_items_pack.comment else ''
        else:
            return None"""

    def get_prices(self, obj):
        return {
            'price': get_price_with_currency(self, obj.total_price),
            'old_price': get_price_with_currency(self, obj.fixed_price) if obj.fixed_price > obj.total_price else None
        }

    def get_status(self, obj):
        return {
            'id': obj.status,
            'title': settings.ORDER_ITEM_STATUSES[obj.status]['title']
        }

    def get_image(self, obj):

        try:
            return settings.SITE_URL + obj.product.image.url
        except:
            return settings.SITE_URL + obj.product.product.image.url
        """if obj.cart_item:
            return obj.cart_item.product.get_image()
        elif obj.cart_items_pack:
            color = obj.cart_items_pack.color
            product = obj.cart_items_pack.product.get_skus_by_filter(color=color).first()
            return product.get_image()
        else:
            return '#'"""

    def get_comment_image(self , obj):
        try:
            photo_obj = OrderItemCommentPhoto.objects.get(order_item=obj)
            return settings.SITE_URL + photo_obj.image.url
        except:
            return '-'


    class Meta:
        model = OrderItem
        fields = [
            'id', 'order',
            'brand', 'title', 'size', 'color', 'change_agreement',
            'comment', 'prices', 'status', 'image', 'comment_image'
        ]
        read_only_fields = ('order',)


class OrderBrandSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        order = self.context.get('order', None)
        currency = self.context.get('currency', 'PLN')
        if order:
            order_items = OrderItemSerializer(
                order.order_items.filter(Q(cart_item__product__product__brand=obj) |
                                         Q(cart_items_pack__product__brand=obj)), many=True,
                context={'currency': currency}).data
            return order_items
        return []

    class Meta:
        model = Brand
        fields = [
            'title', 'items'
        ]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    delivery_address = serializers.SerializerMethodField(read_only=True)
    delivery_method = serializers.SerializerMethodField()
    payment_method = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    specification = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    order_cost = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    delivery_cost = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    def get_delivery_address(self, obj):
        from ..serializers import DeliveryAddressSerializer
        address = DeliveryAddressSerializer(obj.delivery_address).data
        return address

    def get_delivery_method(self, obj):
        return obj.delivery_method.title

    def get_payment_method(self, obj):
        return obj.payment_method.title

    def get_status(self, obj):
        return {
            'id': obj.status,
            'title': settings.ORDER_STATUSES[obj.status]['title']
        }

    def get_specification(self, obj):
        return settings.SITE_URL + obj.specification.url if obj.specification else '#'

    def get_services(self, obj):
        request = self.context.get('request', None)
        if request:
            context = {'request': request}
        else:
            currency = self.context.get('currency', 'PLN')
            context = {'currency': currency}
        return ServiceSerializer(obj.services.all(), many=True, context=context).data

    def get_order_cost(self, obj):
        return get_price_with_currency(self, obj.order_cost)

    def get_discount(self, obj):
        return get_price_with_currency(self, obj.discount)

    def get_delivery_cost(self, obj):
        return get_price_with_currency(self, obj.delivery_cost)

    def get_total_cost(self, obj):
        return get_price_with_currency(self, obj.total_cost)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'cart', 'status', 'comment',
            'payment_method', 'delivery_method', 'delivery_address',
            'track_number', 'specification', 'services',
            'weight', 'order_cost', 'discount', 'delivery_cost', 'total_cost',
            'created_at', 'updated_at',
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    passport = serializers.SerializerMethodField()
    order_items = serializers.SerializerMethodField()
    wait_call = serializers.SerializerMethodField()
    # comment_order = serializers.SerializerMethodField()
    comment_passport = serializers.SerializerMethodField()

    def get_passport(self, obj):
        return PassportMixinSerializer(obj).data

    def get_order_items(self, obj):
        currency = self.context.get('currency', 'PLN')
        return OrderItemSerializer(obj.order_items.all(), many=True, context={'currency': currency}).data

    def get_wait_call(self, obj):
        return ''

    def get_comment_order(self, obj):
        return ''

    def get_comment_passport(self, obj):
        return ''

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'profile', 'cart',
            'order_items', 'payment_method', 'delivery_method', 'passport', 'delivery_address',
            'status', 'extra', 'created_at', 'updated_at',
            'first_name', 'middle_name', 'last_name',
            'passport_number', 'passport_issued', 'passport_issue_date', 'wait_call',
            # 'comment_order',
            'comment_passport',
            'order_cost', 'discount', 'delivery_cost', 'total_services_cost', 'total_cost',
        ]
        extra_kwargs = {
            'delivery_address': {'write_only': True, 'required': True},
            'wait_call': {'write_only': True},
            'comment_order': {'write_only': True},
            'comment_passport': {'write_only': True},
            'cart': {'read_only': True},
            'profile': {'read_only': True},
            'order_items': {'read_only': True},
        }

    def validate(self, attrs):
        data = self.context['request'].data
        attrs['wait_call'] = data.get('wait_call', False)
        attrs['comment'] = data.get('comment_order', '')
        attrs['comment_passport'] = data.get('comment_passport', '')
        attrs['services'] = data.get('services', [])
        return super(OrderCreateSerializer, self).validate(attrs)

    def create(self, validated_data):
        from ..models import Delivery
        user = validated_data.pop('user')
        services = validated_data.pop('services')
        profile = user.profile
        cart = profile.cart
        status = settings.ORDER_STATUS_PAYMENT_WAITING
        validated_data.update({'profile': profile, 'cart': cart, 'status': status})
        items = cart.cart_items.filter(selected=True, pack=None, status=0)
        packs = cart.cart_packs.filter(selected=True, status=0)
        if not items.exists() and not packs.exists():
            return None
        order = Order(**validated_data)
        order.save()
        total_qty = items.aggregate(total_qty=Sum('qty'))['total_qty']
        if profile.role == 1:
            if total_qty < 3:
                Delivery.objects.create(
                    order=order,
                    status='delivery_payment_confirmed',
                    cost=validated_data['delivery_address'].country.delivery_price
                )
        if profile.role == 2:
            Delivery.objects.create(
                order=order,
                status='delivery_payment_waiting',
            )
        order.services.set(services)
        for item in items:
            product = item.product
            qty = item.qty
            for i in range(qty):
                OrderItem.objects.create(
                    order=order,
                    title=product.product.title,
                    product=product,
                    cart_item=item,
                )
            item.status = item.STATUS.ORDERED
            item.save()
        for pack in packs:
            items = pack.cart_pack_items.all()
            for item in items:
                product = item.product
                qty = item.qty
                for i in range(qty):
                    OrderItem.objects.create(
                        order=order,
                        title=product.product.title,
                        product=product,
                        cart_items_pack=pack,
                    )
            pack.status = pack.STATUS.ORDERED
            pack.save()
        order.save()
        order.order_items.all().update(status=settings.ORDER_ITEM_STATUS_PAYMENT_WAITING)
        if profile.role in [2, 3] and profile.balance >= order.total_cost:
            profile.balance -= order.total_cost
            profile.save()
            order.status = settings.ORDER_STATUS_IN_PROCESS
            order.save()
            order.order_items.all().update(status=settings.ORDER_ITEM_STATUS_PAID)
        return order


class OrderListSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(read_only=True)
    delivery_cost = serializers.SerializerMethodField(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    order_cost = serializers.SerializerMethodField()

    def get_order_cost(self, obj):
        return get_price_with_currency(self, obj.order_cost)
    def get_total(self, obj):
        #return get_price_with_currency(self, obj.get_order_total())
        return get_price_with_currency(self, obj.total_cost)

    def get_delivery_cost(self, obj):
        return get_price_with_currency(self, obj.delivery_cost)

    def get_address(self, obj):
        from ..serializers import DeliveryAddressSerializer
        address = DeliveryAddressSerializer(obj.delivery_address).data
        return address

    def get_status(self, obj):
        return {
            'status': obj.status,
            'title': settings.ORDER_STATUSES.get(obj.status)['title']
        }

    def get_url(self, obj):
        return obj.get_absolute_url()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'delivery_method', 'address', 'order_cost', 'total', 'payment_method', 'delivery_cost',
            'status', 'created_at', 'updated_at', 'url', 'slug'
        ]


class OrderCartItemsSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    qty = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    is_pack = serializers.BooleanField(read_only=True, default=False)
    comment = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.product.product.title

    def get_size(self, obj):
        return obj.product.size.get_size_name()

    def get_color(self, obj):
        return obj.product.color.title

    def get_qty(self, obj):
        return obj.qty

    def get_price(self, obj):
        return get_price_with_currency(self, obj.price)

    def get_old_price(self, obj):
        return None if obj.old_price in [0.00, None] else get_price_with_currency(self, obj.old_price)

    def get_total_price(self, obj):
        return get_price_with_currency(self, obj.total_price)

    def get_discount(self, obj):
        return get_price_with_currency(self, obj.discount)

    def get_brand(self, obj):
        return obj.product.product.brand.title

    def get_comment(self, obj):
        return obj.comment.comment if obj.comment else ''

    def get_image(self, obj):
        return obj.product.get_image()

    class Meta:
        model = CartItem
        fields = [
            'id', 'brand', 'title', 'size', 'color',
            'qty', 'price', 'old_price', 'total_price', 'discount',
            'change_agreement', 'is_pack', 'comment', 'image'
        ]


class OrderCartItemPacksSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    qty = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    is_pack = serializers.BooleanField(read_only=True, default=True)
    comment = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.product.title

    def get_size(self, obj):
        return obj.get_sizes()

    def get_color(self, obj):
        return obj.color.title

    def get_qty(self, obj):
        return obj.qty

    def get_price(self, obj):
        return get_price_with_currency(self, obj.price)

    def get_old_price(self, obj):
        return None if obj.old_price in [0.00, None] else get_price_with_currency(self, obj.old_price)

    def get_total_price(self, obj):
        return get_price_with_currency(self, obj.total_price)

    def get_discount(self, obj):
        return get_price_with_currency(self, obj.get_discount())

    def get_brand(self, obj):
        return obj.product.brand.title

    def get_comment(self, obj):
        return obj.comment.comment if obj.comment else ''

    def get_image(self, obj):
        return obj.product.get_image()

    class Meta:
        model = CartItemsPack
        fields = [
            'id', 'brand', 'title', 'size', 'color',
            'qty', 'price', 'old_price', 'total_price', 'discount',
            'change_agreement', 'is_pack', 'comment', 'image'
        ]


class OrderCartBrandsSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    condition = serializers.SerializerMethodField()
    is_performed = serializers.SerializerMethodField()

    def get_items(self, obj):
        cart = self.context.get('cart', None)
        currency = self.context.get('currency', 'PLN')
        if cart:
            cart_packs = CartItemsPack.objects.filter(cart=cart, product__brand=obj, status=0, selected=True)
            cart_items = CartItem.objects.filter(cart=cart, product__product__brand=obj, pack=None,
                                                 product__product__is_in_stock=False, status=0, selected=True)
            serialized_cart_packs = OrderCartItemPacksSerializer(cart_packs, many=True).data
            serialized_cart_items = OrderCartItemsSerializer(cart_items, many=True, context={'currency': currency}).data
            items = serialized_cart_packs + serialized_cart_items
            return items
        return []

    def get_condition(self, obj):
        return obj.brand_rc.__str__()

    def get_is_performed(self, obj):
        cart = self.context.get('cart', None)
        return cart.get_is_performed(obj)

    class Meta:
        model = Brand
        fields = [
            'id', 'title', 'condition',
            'items', 'is_performed'
        ]


class OrderCheckoutSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_items = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_cart_items(self, obj):
        user = self.context['user']
        currency = self.context.get('currency', 'PLN')
        if user.profile.role == 3:
            brands = obj.get_brands()
            serialized_brands = OrderCartBrandsSerializer(brands, many=True, context={'cart': obj}).data
            cart_items = []
            for brand in serialized_brands:
                if len(brand['items']) > 0:
                    cart_items.append(brand)
        else:
            items = obj.cart_items.filter(status=0, pack=None, selected=True)
            cart_items = OrderCartItemsSerializer(items, many=True, context={'currency': currency}).data
        return cart_items

    def get_in_stock(self, obj):
        user = self.context['user']
        currency = self.context.get('currency', 'PLN')
        if user.profile.role == 3:
            in_stock_items = obj.cart_items.filter(pack=None, product__product__is_in_stock=True,
                                                   status=0, selected=True)
            return OrderCartItemsSerializer(in_stock_items, many=True, context={'currency': currency}).data
        return []

    def get_price(self, obj):
        return get_price_with_currency(self, obj.get_cart_total())

    def get_discount(self, obj):
        return get_price_with_currency(self, obj.get_total_discount())

    def get_delivery(self, obj):
        user = self.context['user']
        return obj.get_delivery(user)

    def get_total_price(self, obj):
        user = self.context['user']
        return get_price_with_currency(self, obj.get_cart_total() + obj.get_delivery(user)['price'])

    class Meta:
        model = Cart
        fields = [
            'user', 'price', 'discount', 'delivery', 'total_price', 'cart_items', 'in_stock'
        ]


class UnformedOrderItemSerializer(serializers.ModelSerializer):

    brand = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    qty = serializers.SerializerMethodField()

    def get_brand(self, obj):
        if obj.cart_item:
            return obj.cart_item.product.product.brand.title
        elif obj.cart_items_pack:
            return obj.cart_items_pack.product.brand.title
        else:
            return None

    def get_size(self, obj):
        if obj.cart_item:
            return obj.cart_item.product.size.get_size_name()
        elif obj.cart_items_pack:
            return obj.cart_items_pack.get_sizes()
        else:
            return None

    def get_color(self, obj):
        if obj.cart_item:
            return obj.cart_item.product.color.title
        elif obj.cart_items_pack:
            return obj.cart_items_pack.color.title
        else:
            return None

    def get_comment(self, obj):
        return {
            'text': obj.comment,
            'images': OrderCorrespondenceImageSerializer(obj.order_item_comment_photos.all(), many=True).data,
        }

    def get_status(self, obj):
        return {
            'id': obj.status,
            'title': settings.ORDER_ITEM_STATUSES[obj.status]['title']
        }

    def get_image(self, obj):
        if obj.cart_item:
            return obj.cart_item.product.get_image()
        elif obj.cart_items_pack:
            color = obj.cart_items_pack.color
            product = obj.cart_items_pack.product.get_skus_by_filter(color=color).first()
            return product.get_image()
        else:
            return '#'

    def get_price(self, obj):
        return get_price_with_currency(self, obj.total_price)

    def get_qty(self, obj):
        return 1

    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'price', 'image', 'qty',
            'brand', 'title', 'size', 'color',
            'change_agreement', 'comment',
        ]
        read_only_fields = ('order',)


class UnformedOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_items = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_cart_items(self, obj):
        user = self.context['user']
        currency = self.context.get('currency', 'PLN')
        if user.profile.role == 3:
            # todo переделать для опта
            brands = obj.get_brands()
            serialized_brands = OrderCartBrandsSerializer(brands, many=True, context={'cart': obj}).data
            cart_items = []
            for brand in serialized_brands:
                if len(brand['items']) > 0:
                    cart_items.append(brand)
        else:
            items = obj.order_items.all()
            cart_items = UnformedOrderItemSerializer(items, many=True, context={'currency': currency}).data
        return cart_items

    def get_in_stock(self, obj):
        user = self.context['user']
        currency = self.context.get('currency', 'PLN')
        if user.profile.role == 3:
            in_stock_items = obj.cart.cart_items.filter(pack=None, product__product__is_in_stock=True,
                                                   status=0, selected=True)
            return OrderCartItemsSerializer(in_stock_items, many=True, context={'currency': currency}).data
        return []

    def get_price(self, obj):
        return get_price_with_currency(self, obj.cart.get_cart_total())

    def get_discount(self, obj):
        return get_price_with_currency(self, obj.cart.get_total_discount())

    def get_delivery(self, obj):
        user = self.context['user']
        return obj.cart.get_delivery(user)

    def get_total_price(self, obj):
        user = self.context['user']
        return get_price_with_currency(self, obj.cart.get_cart_total() + obj.cart.get_delivery(user)['price'])

    class Meta:
        model = Order
        fields = [
            'user', 'price', 'discount', 'delivery', 'total_price', 'cart_items', 'in_stock'
        ]


def get_price_with_currency(data, price):
    try:
        if 'request' in data.context.keys():
            currency_title = data.context['request'].headers.get('currency', 'PLN')
        else:
            currency_title = data.context['currency']
        currency = Currency.objects.get(title=currency_title).ratio
    except:
        currency = Decimal('1.0000')
    price = price / currency
    return price.__round__(2)

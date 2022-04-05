from decimal import Decimal
from garpix_catalog.models import Brand, Currency, ProductSku, Product
from rest_framework import serializers
from ..models import Cart, CartItem, CartItemsPack
from django.db.models import Sum
import random



class CartItemProductSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.title

    def get_brand(self, obj):
        return obj.brand.title

    def get_image(self, obj):
        return obj.get_image()

    class Meta:
        model = Product
        fields = ['id', 'brand', 'title', 'image']


class CartItemProductSkuSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_brand(self, obj):
        return obj.product.brand.title

    def get_title(self, obj):
        return obj.product.title

    def get_size(self, obj):
        return obj.size.get_size_name()

    def get_color(self, obj):
        return obj.color.title

    def get_image(self, obj):
        return obj.get_image()

    class Meta:
        model = ProductSku
        fields = ['id', 'brand', 'title', 'size', 'color', 'image', 'in_stock_count']


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    condition = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()
    total_item_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    is_pack = serializers.SerializerMethodField()#serializers.BooleanField(read_only=True, default=False)
    is_collection = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_product(self, obj):
        return CartItemProductSkuSerializer(obj.product, many=False).data

    def get_condition(self, obj):
        return obj.product.product.product_rc.__str__() if obj.product.product.product_rc else None

    def get_price(self, obj):
        return get_price_with_currency(self, obj.price)

    def get_old_price(self, obj):
        return None if obj.old_price in [0.00, None] else get_price_with_currency(self, obj.old_price)

    def get_total_item_price(self, obj):
        return get_price_with_currency(self, obj.total_item_price)

    def get_total_price(self, obj):
        return get_price_with_currency(self, obj.total_price)

    def get_color(self, obj):
        return obj.product.color.title

    def get_size(self, obj):
        return obj.product.size.get_size_name()

    def get_url(self, obj):
        return obj.product.product.get_absolute_url()

    def get_is_pack(self, obj):
        #return obj.product.product.product_rc.rc_type
        try:
            if obj.product.product.product_rc.rc_type == 2:
                return True
            else:
                return False
        except:
            return False
    def get_is_collection(self, obj):
        try:
            if obj.product.product.product_rc.rc_type == 1:
                return True
            else:
                return False
        except:
            return False


    class Meta:
        model = CartItem
        fields = [
            'id', 'cart', 'is_pack', 'is_collection',
            'qty', 'selected', 'price', 'old_price', 'total_item_price', 'total_price',
            'condition',
            'change_agreement',
            'product', 'url', 'color', 'size',
        ]
        read_only_fields = ('cart',)


class CartBrandSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    condition = serializers.SerializerMethodField()
    is_performed = serializers.SerializerMethodField()
    is_selected = serializers.SerializerMethodField()

    def get_items(self, obj):
        cart = self.context.get('cart', None)
        user = self.context['user']
        currency = self.context['currency']
        if cart:
            cart_packs = CartItemsPackSerializer(
                CartItemsPack.objects.filter(cart=cart, product__brand=obj, status=0), many=True,
                context={'user': user, 'currency': currency}).data
            cart_items = CartItemSerializer(
                CartItem.objects.filter(
                    cart=cart, product__product__brand=obj, pack=None, product__product__is_in_stock=False, status=0
                ), many=True, context={'user': user, 'currency': currency}).data
            items = cart_packs + cart_items
            return items
        return []

    def get_condition(self, obj):
        return obj.brand_rc.__str__()

    def get_is_performed(self, obj):
        cart = self.context.get('cart', None)
        return cart.get_is_performed(obj)

    def get_is_selected(self, obj):
        cart = self.context.get('cart', None)
        return cart.get_is_selected(obj)

    class Meta:
        model = Brand
        fields = [
            'id', 'title', 'condition', 'items', 'is_performed', 'is_selected'
        ]


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cartitem_set = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    selected = serializers.SerializerMethodField()
    in_cart = serializers.SerializerMethodField()
    total_discount = serializers.SerializerMethodField()
    delivery_price = serializers.SerializerMethodField()
    cart_ids = serializers.SerializerMethodField()

    def get_cartitem_set(self, obj):
        user = self.context['user']
        currency = self.context['currency']
        if user.profile.role == 3:
            brands = obj.get_brands()
            cart_items = CartBrandSerializer(brands, many=True, context={
                'cart': obj, 'user': user, 'currency': currency}).data
        else:
            cart_items = CartItemSerializer(obj.cart_items.filter(status=0, pack=None), many=True,
                                            context={'user': user, 'currency': currency}).data
        return cart_items

    def get_total_price(self, obj):
        return get_price_with_currency(self, obj.get_cart_total())

    def get_in_stock(self, obj):
        user = self.context['user']
        currency = self.context['currency']
        if user.profile.role == 3:
            in_stock_items = obj.cart_items.filter(pack=None, product__product__is_in_stock=True, status=0)
            return CartItemSerializer(in_stock_items, many=True, context={'user': user, 'currency': currency}).data
        return []

    def get_selected(self, obj):
        user = self.context['user']
        items_selected = obj.get_selected_items().aggregate(selected=Sum('qty'))['selected']
        total_selected = items_selected if items_selected else 0
        if user.profile.role == 3:
            pack_items_selected = obj.get_selected_packs().aggregate(selected=Sum('qty'))['selected']
            total_selected = total_selected + pack_items_selected if pack_items_selected else total_selected
        return total_selected

    def get_in_cart(self, obj):
        user = self.context['user']
        items_count = obj.get_in_cart_items().aggregate(items_count=Sum('qty'))['items_count']
        total_items_count = items_count if items_count else 0
        if user.profile.role == 3:
            pack_items_count = obj.get_in_cart_packs().aggregate(pack_items_count=Sum('qty'))['pack_items_count']
            total_items_count = total_items_count + pack_items_count if pack_items_count else total_items_count
        return total_items_count

    def get_total_discount(self, obj):
        return get_price_with_currency(self, obj.get_total_discount())

    def get_delivery_price(self, obj):
        user = self.context['user']
        return get_price_with_currency(self, obj.get_delivery(user)['price'])

    def get_cart_ids(self, obj):
        cart_items = CartItem.objects.filter(cart=obj, status=0)#obj.cart_items
        cart_items_ids = []
        for tt in cart_items:
            cart_items_ids.append(tt.id)
        return cart_items_ids

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'created_at', 'updated_at', 'cartitem_set', 'in_stock',
            'in_cart', 'selected', 'total_price', 'total_discount', 'delivery_price', 'cart_ids'
        ]


class CartAddItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        item = CartItem.objects.create(
            cart=validated_data['cart'],
            price=validated_data['price'],
            qty=validated_data['qty'],
            product=validated_data['product']
        )
        return item

    class Meta:
        model = CartItem
        fields = ['cart', 'price', 'qty', 'product']
        extra_kwargs = {
            'cart': {'read_only': True},
            'price': {'read_only': True}
        }


class CartMultipleAddSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cartitem_set = serializers.SerializerMethodField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, source='get_cart_total', read_only=True)
    products = serializers.ListField(write_only=True)

    def get_cartitem_set(self, obj):
        cart_items = CartItemSerializer(obj.cart_items.filter(status=0), many=True).data
        return cart_items

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'total', 'cartitem_set', 'products']


class CartDelItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'qty']
        extra_kwargs = {
            'product': {'required': True}
        }


class CartItemsPackSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    condition = serializers.SerializerMethodField()
    is_pack = serializers.BooleanField(read_only=True, default=True)
    url = serializers.SerializerMethodField()

    def get_product(self, obj):
        return CartItemProductSerializer(obj.product, many=False).data

    def get_price(self, obj):
        return get_price_with_currency(self, obj.price)

    def get_old_price(self, obj):
        return None if obj.old_price in [0.00, None] else get_price_with_currency(self, obj.old_price)

    def get_total_price(self, obj):
        return get_price_with_currency(self, obj.total_price)

    def get_color(self, obj):
        return obj.color.title if obj.color else None

    def get_size(self, obj):
        return obj.get_sizes()

    def get_condition(self, obj):
        return obj.product.product_rc.__str__() if obj.product.product_rc else None

    def get_url(self, obj):
        return obj.product.get_absolute_url()

    class Meta:
        model = CartItemsPack
        fields = [
            'id', 'cart', 'is_pack',
            'qty', 'selected', 'price', 'old_price', 'total_price',
            'condition',
            'change_agreement', 'url',
            'product', 'color', 'size',
        ]
        read_only_fields = ('cart',)


class CartAddPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItemsPack
        fields = [
            'id', 'cart',
            'product', 'color', 'size', 'condition',
            'qty', 'in_pack_count', 'total_count',
            'price', 'old_price', 'total_price',
            'selected',
        ]


def get_price_with_currency(data, price):
    try:
        currency_title = data.context['currency']
        currency = Currency.objects.get(title=currency_title).ratio
    except:
        currency = Decimal('1.0000')
    price = price / currency
    return price.__round__(2)

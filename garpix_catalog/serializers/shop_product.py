from rest_framework import serializers
from ..models import Product, Currency, ShopProduct
from django.conf import settings
from shop.models import Shop


class CabinetProductMainListSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    price_for_me = serializers.SerializerMethodField()
    recommended_price = serializers.SerializerMethodField()
    your_price = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.get_image()

    def get_price_for_me(self, obj):
        return obj.dropshipper_total_price_auto

    def get_recommended_price(self, obj):
        return obj.retailer_total_price_auto

    def get_your_price(self, obj):
        shop = self.context['request'].user.profile.profile_shop
        markup = obj.category.category_markups.filter(shop=shop).first()
        if markup and markup.markup != 0:
            return obj.dropshipper_total_price_auto + markup.markup
        return obj.retailer_total_price_auto

    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'price_for_me', 'recommended_price', 'your_price']


class CabinetProductMyListSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price_for_me = serializers.SerializerMethodField()
    recommended_price = serializers.SerializerMethodField()
    your_price = serializers.SerializerMethodField()

    def get_id(self, obj):
        shop = self.context['request'].user.profile.profile_shop
        return ShopProduct.get_shop_product(shop_id=shop.id, product_id=obj.id).id

    def get_image(self, obj):
        return obj.get_image()

    def get_price_for_me(self, obj):
        return obj.dropshipper_total_price_auto

    def get_recommended_price(self, obj):
        return obj.retailer_total_price_auto

    def get_your_price(self, obj):
        shop = self.context['request'].user.profile.profile_shop
        return ShopProduct.get_shop_product(shop_id=shop.id, product_id=obj.id).total_price_auto

    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'price_for_me', 'recommended_price', 'your_price']


class CabinetCreateProductSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price_for_me = serializers.SerializerMethodField()
    your_price = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.product.title

    def get_image(self, obj):
        return obj.product.get_image()

    def get_price_for_me(self, obj):
        return obj.purchase_price

    def get_your_price(self, obj):
        return obj.total_price_auto

    class Meta:
        model = ShopProduct
        fields = ['product', 'shop', 'id', 'title', 'image', 'price_for_me', 'recommended_price', 'price', 'your_price']

        extra_kwargs = {
            'title': {'required': False},
            'product': {'write_only': True},
            'shop': {'write_only': True},
            'price': {'write_only': True},
        }
        
    def validate(self, attrs):
        data = self.context['request'].data
        product = Product.objects.filter(id=data.get('product_id', None)).first()
        attrs.update({'product': product})
        return super(CabinetCreateProductSerializer, self).validate(attrs)


class CabinetUpdateProductSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price_for_me = serializers.SerializerMethodField()
    your_price = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.product.title

    def get_image(self, obj):
        return obj.product.get_image()

    def get_price_for_me(self, obj):
        return obj.purchase_price

    def get_your_price(self, obj):
        return obj.total_price_auto

    class Meta:
        model = ShopProduct
        fields = ['id', 'title', 'image', 'price_for_me', 'recommended_price', 'price', 'your_price']

        extra_kwargs = {
            'price': {'write_only': True}
        }


def get_user(data):
    if 'user' in data.context.keys():
        return data.context['user']
    return data.context['request'].user


def get_currency(data):
    if 'currency' in data.context.keys():
        currency_title = data.context['currency']
    elif 'request' in data.context.keys():
        try:
            currency_title = data.context['request'].headers.get('currency', 'PLN')
        except Exception:
            currency_title = 'PLN'
    else:
        currency_title = 'PLN'
    if currency_title not in ['PLN', None]:
        currency = Currency.objects.filter(title=currency_title).first()
        return currency.ratio
    return 1.0000


def get_prices(obj, user=None, currency=None):
    prices = obj.get_prices(user, currency)
    prices['price'] = (prices['price']).__round__(2)
    prices['old_price'] = (prices['old_price']).__round__(2) if prices['old_price'] else None
    return prices


def get_filters(data):
    try:
        size = data.context['request'].GET.get('size', None)
    except:
        size = None
    try:
        color = data.context['request'].GET.get('color', None)
    except:
        color = None
    return {'size': size, 'color': color}


def get_skus_by_filters(filters):
    return

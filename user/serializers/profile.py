from decimal import Decimal
from django.conf import settings
from django.db.models import Sum
from rest_framework import serializers
from ..models import Profile
from .user import UserSerializer
from garpix_order.serializers import DeliveryAddressSerializer
from garpix_catalog.models import Currency


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)
    organization = serializers.SerializerMethodField(read_only=True)
    passport = serializers.SerializerMethodField(read_only=True)
    shop = serializers.SerializerMethodField(read_only=True)
    addresses = serializers.SerializerMethodField(read_only=True)
    balance = serializers.SerializerMethodField(read_only=True)
    passive_balance = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    cart = serializers.SerializerMethodField(read_only=True)
    wishlist = serializers.SerializerMethodField(read_only=True)
    notifications = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def get_links(self, obj):
        return {
            'vk_link': obj.vk_link,
            'insta_link': obj.insta_link,
            'site_link': obj.site_link,
        }

    def get_organization(self, obj):
        return {
            'inn': obj.inn,
            'organization': obj.organization,
        }

    def get_passport(self, obj):
        return {
            'passport_number': obj.passport_number,
            'passport_issued': obj.passport_issued,
            'passport_issue_date': obj.passport_issue_date,
        }

    def get_shop(self, obj):
        if hasattr(obj, 'profile_shop') and obj.profile_shop.is_active:
            return {
                'is_has_shop': True,
                'shop_link': obj.profile_shop.site.domain,
                'shop_id': obj.profile_shop.id,
                'shop_title': obj.profile_shop.title,
                'shop_logo': settings.SITE_URL + obj.profile_shop.logo.url if obj.profile_shop.logo.url else '#',
            }
        return {
            'is_has_shop': False,
        }

    def get_addresses(self, obj):
        addresses = obj.profile_addresses.all()
        return DeliveryAddressSerializer(addresses, many=True).data

    def get_balance(self, obj):
        return get_price_with_currency(self, obj.balance)

    def get_passive_balance(self, obj):
        pb = obj.profile_payments.filter(status=0).aggregate(passive_balance=Sum('cost'))['passive_balance']
        if pb:
            return get_price_with_currency(self, pb)
        return Decimal(0.00)

    def get_status(self, obj):
        return obj.user.status

    def get_cart(self, obj):
        items_count = obj.cart.get_in_cart_items().aggregate(items_count=Sum('qty'))['items_count']
        total_items_count = items_count if items_count else 0
        if obj.role == 3:
            pack_items_count = obj.cart.get_in_cart_packs().aggregate(pack_items_count=Sum('qty'))['pack_items_count']
            total_items_count = total_items_count + pack_items_count if pack_items_count else total_items_count
        return total_items_count

    def get_wishlist(self, obj):
        from ..models.wishlist_item import WishListItem
        return WishListItem.objects.filter(profile=obj).count()

    def get_notifications(self, obj):
        from ..models.notification import Notification
        return Notification.objects.filter(profile=obj, is_read=False).count()

    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'links',
            'organization',
            'passport',
            'role',
            'shop',
            'addresses',
            'balance',
            'passive_balance',
            'status',
            'cart',
            'wishlist',
            'balance',
            'notifications',
            'receive_newsletter',
        )


def get_price_with_currency(data, price):
    try:
        currency_title = data.context['currency']
        currency = Currency.objects.get(title=currency_title).ratio
    except:
        currency = Decimal('1.0000')
    price = price / currency
    return price.__round__(2)

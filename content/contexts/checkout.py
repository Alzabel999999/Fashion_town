from decimal import Decimal
from django.conf import settings
from .common import common_context
from ..serializers import PageSerializer
from garpix_order.serializers import (
    OrderCheckoutSerializer, PaymentMethodSerializer, DeliveryMethodSerializer, UnformedOrderSerializer
)
from garpix_order.models import PaymentMethod, DeliveryMethod, Order, OrderItem
from garpix_catalog.models import Currency
import time
import os


def context(request, **kwargs):

    page = kwargs['object']
    user = kwargs['user']
    currency = request.headers.get('currency', 'PLN')

    profile = user.profile
    unformed_order = Order.get_unformed_order(profile)
    unformed_order.order_items.all().delete()

    cart = profile.cart

    for cart_item in cart.get_selected_items():
        product = cart_item.product
        title = product.product.title
        price = 0.0
        fixed_price = cart_item.total_item_price
        total_price = cart_item.total_item_price
        OrderItem.objects.bulk_create([
            OrderItem(
                order=unformed_order,
                title=title,
                price=price,
                product=product,
                fixed_price=fixed_price,
                total_price=total_price,
                cart_item=cart_item,
            ) for n in range(cart_item.qty)
        ])

    Order.objects.filter(id=unformed_order.id).update(cart=cart)
    Order.objects.filter(id=unformed_order.id).update(
        order_cost=cart.get_cart_total(),
        discount=cart.get_total_discount(),
        delivery_cost=cart.get_delivery(user)['price'],
        total_cost=cart.get_cart_total() + cart.get_delivery(user)['price'],
        comment='',
        delivery_address=None,
        delivery_method=None,
        payment_method=None,
        wait_call=False,
    )

    cart_content = UnformedOrderSerializer(
        unformed_order, many=False, context={'user': user, 'currency': currency}).data

    if profile and profile.role in [2, 3]:
        payment_methods = PaymentMethodSerializer(PaymentMethod.objects.all(), many=True).data
    else:
        payment_methods = PaymentMethodSerializer(
            PaymentMethod.objects.filter(type=settings.PAYMENT_TYPE_ONLINE), many=True).data

    if profile and profile.role == 3:
        delivery_methods = DeliveryMethodSerializer(
            DeliveryMethod.objects.filter(type__in=[
                settings.DELIVERY_TYPE_CARGO_WITH_DOCS, settings.DELIVERY_TYPE_CARGO_WITHOUT_DOCS]), many=True).data
    elif profile and profile.role == 2:
        delivery_methods = DeliveryMethodSerializer(
            DeliveryMethod.objects.filter(type__in=[
                settings.DELIVERY_TYPE_POLAND_POST, settings.DELIVERY_TYPE_POLAND_CDEK,
                settings.DELIVERY_TYPE_RUSSIA_POST, settings.DELIVERY_TYPE_RUSSIA_SDEK, settings.DELIVERY_TYPE_CARGO_FIVE_KG]), many=True).data
    else:
        delivery_methods = DeliveryMethodSerializer(
            DeliveryMethod.objects.filter(type__in=[
                settings.DELIVERY_TYPE_CDEK, settings.DELIVERY_TYPE_POST]), many=True).data

    context = {
        'page_info': PageSerializer(page).data,
        'cart_content': cart_content,
        'payment_methods': payment_methods,
        'delivery_methods': delivery_methods,
    }
    context.update(common_context(user, page))

    return context


def get_price_with_currency(currency_title, price):
    currency = Currency.objects.get(title=currency_title).ratio
    price = price / currency
    return price.__round__(2)

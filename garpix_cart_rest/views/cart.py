import django_filters
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from user.permissions import IsOwnerOrReject
from ..serializers import (
    CartSerializer,
    CartItemSerializer,
    CartAddItemSerializer,
    CartAddPackSerializer,
    CartDelItemSerializer,
    CartMultipleAddSerializer,
    CartItemsPackSerializer,
)
from ..models import Cart, CartItem, CartItemsPack
from rest_framework.response import Response
from garpix_catalog.models import Color, Size, ProductSku, Product
from decimal import Decimal
from garpix_order.serializers.order import OrderCartItemPacksSerializer, OrderCartItemsSerializer


class CartUnauthFilter(django_filters.FilterSet):
    products = django_filters.BaseInFilter(field_name='cart_items__product__size', lookup_expr='in')
    class Meta:
        model = Cart
        fields = ('products',)


class CartViewSet(ViewSet, GenericViewSet):

    queryset = Cart.objects.filter(is_active=True)
    pagination_class = None
    permission_classes = [IsOwnerOrReject, ]

    def get_serializer_class(self):
        if self.action in ['my_cart', 'update_cart', 'select_all', 'unselect_all', 'add_or_modify']:
            return CartSerializer
        if self.action == 'add_to_cart':
            return CartAddItemSerializer
        if self.action == 'add_pack_to_cart':
            return CartAddPackSerializer
        if self.action == 'del_from_cart':
            return CartDelItemSerializer
        if self.action == 'add_comment':
            is_pack = self.request.data.get('is_pack', None)
            if is_pack in (True, 'True', 'true'):
                return OrderCartItemPacksSerializer
            else:
                return OrderCartItemsSerializer
        else:
            return CartSerializer

    @action(methods=['GET', ], detail=False)
    def my_cart(self, request, *args, **kwargs):
        user = request.user
        currency = request.headers.get('currency', 'PLN')
        if user and user.is_authenticated:
            cart = Cart.objects.filter(profile=user.profile).first()
            if not cart:
                return Response({'error': 400}, status=400)
            serializer = self.get_serializer_class()
            data = serializer(cart, many=False, context={'user': user, 'currency': currency}).data
            data['total_order_price'] = Decimal('0.00')
            data['total_order_price'] += Decimal(data['total_price']) if data['total_price'] else Decimal('0.00')
            data['total_order_price'] += data['delivery_price']
            data['is_performed'] = True
            if user.profile.role in [1, 2]: # [1,2]
                unchecked_cart_items = 0
                for cart_item in data['cartitem_set']:
                    if not cart_item['selected']: unchecked_cart_items += 1
                if unchecked_cart_items == len(data['cartitem_set']):
                    data['is_performed'] = False
            elif user.profile.role == 3:
                selected_count = 0
                for cart_item in data['cartitem_set']:
                    performed = True if 'is_performed' in cart_item.keys() and cart_item['is_performed'] else False
                    selected = False
                    if 'is_selected' in cart_item.keys() and cart_item['is_selected']:
                        selected = True
                        selected_count += 1
                    if selected and not performed: data['is_performed'] = False
                for in_stock_item in data['in_stock']:
                    if in_stock_item['selected']: selected_count += 1
                if selected_count == 0: data['is_performed'] = False
            else:
                return Response({'error': 403}, status=403)
            return Response(data)
        return Response({'error': 403}, status=403)

    @action(methods=['POST', ], detail=False)
    def add_or_modify(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user and user.is_authenticated:
            cart = Cart.objects.filter(profile=user.profile).first()
            qty = data.get('qty', 1)
            is_pack = data.get('is_pack', None)
            is_collection = data.get('is_collection', None)
            color = data.get('color', None)
            size = data.get('size', None)
            pid = data.get('product', None)
            product = Product.objects.filter(id=pid).first()
            if is_pack in (True, 'True', 'true'):
                if not product or not color or (product.get_condition().rc_type == 2 and not size):
                    return Response({'error': 400}, status=status.HTTP_400_BAD_REQUEST)
                packs = cart.cart_packs.filter(product=product, status=0, color=color, size=size)
                pack = packs.first()
                if pack:
                    if qty == 0:
                        pack.delete()
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    else:
                        pack.qty = qty
                        pack.save()
                else:
                    pack = CartItemsPack.add_pack(pid=pid, cart=cart, color=color, size=size, qty=1)


                """if pack:
                    if qty == 0:
                        pack.delete()
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    else:
                        pack.qty = qty
                        pack.save()
                else:
                    pack = CartItemsPack.add_pack(pid=pid, cart=cart, color=color, size=size, qty=1)"""
            elif is_collection in (True, 'True', 'true') and user.profile.role == 3:

                sizes = product.product_rc.sizes.all()
                for size in sizes:
                    try:
                        sku = ProductSku.objects.get(product=product, size=size, color=color)
                    except:
                        sku = ProductSku(product=product, size=size, color=color)
                        sku.save()
                    item = CartItem.objects.filter(product=sku, cart=cart, pack=None, status=0).first()
                    if item:
                        if qty == 0:
                            item.delete()
                            return Response(status=status.HTTP_204_NO_CONTENT)
                        else:
                            item.qty = qty
                            item.save()
                            #return Response(status=status.HTTP_200_OK)
                    else:
                        item = CartItem.add_item(sku=sku, cart=cart, qty=1, role=user.profile.role)
                cart.set_items_discount()

            else:
                if product and color and size:
                    sku = product.product_skus.filter(color__id=color, size__id=size).first()
                else:
                    sku = None
                if not sku:
                    return Response({'error': 400}, status=status.HTTP_400_BAD_REQUEST)


                item = CartItem.objects.filter(product=sku, cart=cart, pack=None, status=0).first()
                if item:
                    if qty == 0:
                        item.delete()
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    else:
                        item.qty = qty
                        item.save()
                        #return Response(status=status.HTTP_200_OK)
                else:
                    item = CartItem.add_item(sku=sku, cart=cart, qty=1, role=user.profile.role)
                    #if item != None:
                        #return Response({'cart': item}, status=status.HTTP_200_OK)
                cart.set_items_discount()
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 403}, status=403)

    @action(methods=['POST', ], detail=False)
    def add_to_cart(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user and user.is_authenticated:
            cart = Cart.objects.filter(profile=user.profile).first()
            qty = data.get('qty', 1)
            color = data.get('color', 1)
            size = data.get('size', 1)
            pid = data.get('product', None)
            sku = ProductSku.objects.filter(product__id=pid, color__id=color, size__id=size).first()
            if not sku:
                return Response({'error': 400}, status=400)
            item = CartItem.add_item(sku=sku, cart=cart, qty=qty, role=user.profile.role)
            serializer = self.get_serializer(item)
            return Response(serializer.data, status=201)
        return Response({'error': 403}, status=403)

    # временно вырезано... возможно насовсем)
    # @action(methods=['POST', ], detail=False)
    # def multiple_add_to_cart(self, request, *args, **kwargs):
    #     data = request.data
    #     user = request.user
    #     if user and user.is_authenticated:
    #         cart = Cart.objects.filter(profile=user.profile).first()
    #         products = data.get('products', [])
    #         if not products:
    #             return Response({'error': 400}, status=400)
    #         for product in products:
    #             qty = product.get('qty', 1)
    #             pid = product.get('product', None)
    #             if pid:
    #                 item = CartItem.add_item(pid=pid, cart=cart, qty=qty, role=user.profile.role)
    #         serializer = self.get_serializer(cart)
    #         return Response(serializer.data, status=201)
    #     return Response({'error': 403}, status=403)

    @action(methods=['POST', ], detail=False)
    def add_pack_to_cart(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user and user.is_authenticated and user.profile.role == 3:
            cart = Cart.objects.filter(profile=user.profile).first()
            qty = data.get('qty', 1)
            pid = data.get('product', None)
            color_id = data.get('color', None)
            color = Color.objects.filter(id=color_id).first() if color_id else None
            size_id = data.get('size', None)
            size = Size.objects.filter(id=size_id).first() if size_id else None
            if not pid:
                return Response({'error': 400}, status=400)
            pack = CartItemsPack.add_pack(pid=pid, cart=cart, color=color, size=size, qty=qty)
            serializer = self.get_serializer(pack)
            return Response(serializer.data, status=201)
        return Response({'error': 403}, status=403)

    @action(methods=['DELETE', ], detail=False)
    def del_from_cart(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user and user.is_authenticated:
            cart = Cart.objects.filter(profile=user.profile).first()
            data.update({'cart': cart.id})
            item_id = data.get('item_id', None)
            #is_collection = data.get('is_collection', None)
            if item_id:
                item = CartItem.objects.filter(cart=cart, id=item_id).first()
                rc_type = item.product.product.product_rc.rc_type
                if rc_type == 1 and user.profile.role == 3:
                    product = item.product.product
                    sizes = product.product_rc.sizes.all()
                    for size in sizes:
                        sku = CartItem.objects.filter(product__product=product, product__size=size, cart=cart, pack=None, status=0).first().product
                        item = CartItem.objects.filter(product=sku, cart=cart, pack=None, status=0).first()
                        if item:
                            item.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    if item:
                        if not item.pack:
                            item.delete()
                            return Response(status.HTTP_204_NO_CONTENT)
            return Response(status.HTTP_400_BAD_REQUEST)
        return Response(status.HTTP_403_FORBIDDEN)

    @action(methods=['DELETE', ], detail=False)
    def del_pack_from_cart(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user and user.is_authenticated:
            cart = Cart.objects.filter(profile=user.profile).first()
            data.update({'cart': cart.id})
            item_id = data.get('item_id', None)
            if item_id:
                item = CartItemsPack.objects.filter(cart=cart, id=item_id).first()
                if item:
                    item.delete()
                    return Response(status.HTTP_204_NO_CONTENT)
            return Response(status.HTTP_400_BAD_REQUEST)
        return Response(status.HTTP_403_FORBIDDEN)

    @action(methods=['DELETE', ], detail=False)
    def multiple_del_from_cart(self, request, *args, **kwargs):
        items = request.data.get('items', [])
        user = request.user
        if user and user.is_authenticated:
            cart = Cart.objects.filter(profile=user.profile).first()
            for item in items:
                if item['is_pack']:
                    item_id = item.get('item_id', None)
                    if item_id:
                        item = CartItemsPack.objects.filter(cart=cart, id=item_id).first()
                        if item:
                            item.delete()
                        try:
                            item = CartItem.objects.filter(cart=cart, id=item_id).first()
                            if item:
                                item.delete()
                        except:
                            pass

                else:
                    item_id = item.get('item_id', None)
                    if item_id:
                        item = CartItem.objects.filter(cart=cart, id=item_id).first()
                        if item:
                            if not item.pack:
                                item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['POST', ], detail=False)
    def update_cart(self, request, *args, **kwargs):
        user = request.user
        currency = request.headers.get('currency', 'PLN')
        if user and user.is_authenticated:
            cart = user.profile.cart
            data = request.data



            for item in data:
                qty = item['qty']
                product = CartItem.objects.filter(id=item['id'], cart=cart, pack=None, status=0).first().product.product
                rc_type = product.product_rc.rc_type
                if 'is_pack' in item.keys() and item['is_pack']:
                    cart_items_pack = CartItemsPack.objects.filter(cart=cart, id=item['id'], status=0).first()
                    if cart_items_pack:
                        cart_items_pack.update_items_pack(item)

                elif rc_type == 1 and user.profile.role == 3:
                    sizes = product.product_rc.sizes.all()
                    for size in sizes:
                        sku = CartItem.objects.filter(product__product=product, product__size=size, cart=cart, pack=None, status=0).first().product
                        item_n = CartItem.objects.filter(product=sku, cart=cart, pack=None, status=0).first()
                        if item:
                            if qty == 0:
                                item_n.delete()
                                return Response(status=status.HTTP_204_NO_CONTENT)
                            else:
                                item_n.qty = qty

                                item_n.save()
                                #cart_item = CartItem.objects.filter(cart=cart, id=item.id, status=0).first()

                    cart_item = CartItem.objects.filter(cart=cart, id=item['id'], status=0).first()
                    if cart_item:
                        cart_item.update_item(item)
                else:
                    cart_item = CartItem.objects.filter(cart=cart, id=item['id'], status=0).first()
                    if cart_item:
                        cart_item.update_item(item)
                        #return Response({'update': 'true'}, status=200)
            serializer = self.get_serializer_class()
            cart.set_items_discount()

            data = serializer(cart, many=False, context={'user': user, 'currency': currency}).data
            data['is_performed'] = True
            if user.profile.role in [1, 2]: # [1,2]
                unchecked_cart_items = 0
                for cart_item in data['cartitem_set']:
                    if not cart_item['selected']: unchecked_cart_items += 1
                if unchecked_cart_items == len(data['cartitem_set']):
                    data['is_performed'] = False
            elif user.profile.role == 3:
                selected_count = 0
                for cart_item in data['cartitem_set']:
                    performed = True if 'is_performed' in cart_item.keys() and cart_item['is_performed'] else False
                    selected = False
                    if 'is_selected' in cart_item.keys() and cart_item['is_selected']:
                        selected = True
                        selected_count += 1
                    if selected and not performed: data['is_performed'] = False

                for in_stock_item in data['in_stock']:
                    if in_stock_item['selected']: selected_count += 1
                if selected_count == 0: data['is_performed'] = False
            return Response(data)
        return Response({'error': 403}, status=403)

    @action(methods=['POST', ], detail=False)
    def add_comment(self, request, *args, **kwargs):
        user = request.user
        currency = request.headers.get('currency', 'PLN')
        if user and user.is_authenticated:
            cart = user.profile.cart
            item_id = request.data.get('id', None)
            if not item_id:
                return Response({'error': 400}, status=400)
            comment = request.data.get('comment', '')
            files = request.FILES.getlist('files', [])
            is_pack = request.data.get('is_pack', None)
            if is_pack in (True, 'True', 'true'):
                pack = CartItemsPack.objects.filter(cart=cart, id=item_id, status=0).first()
                if not pack:
                    return Response({'error': 400}, status=400)
                pack.add_comment(comment, files)
                item = pack
            else:
                item = CartItem.objects.filter(cart=cart, id=item_id).first()#status=0
                if not item:
                    return Response({'error': 401}, status=400)
                item.add_comment(comment, files)
            serializer = self.get_serializer_class()
            return Response(serializer(item, context={'user': user, 'currency': currency}).data)
        return Response({'error': 403}, status=403)

    @action(methods=['POST', ], detail=False)
    def select_all(self, request, *args, **kwargs):
        user = request.user
        currency = request.headers.get('currency', 'PLN')
        if user and user.is_authenticated:
            cart = user.profile.cart
            cart = cart.select_all()
            serializer = self.get_serializer_class()
            return Response(serializer(cart, many=False, context={'user': user, 'currency': currency}).data)
        return Response({'error': 403}, status=403)

    @action(methods=['POST', ], detail=False)
    def unselect_all(self, request, *args, **kwargs):
        user = request.user
        currency = request.headers.get('currency', 'PLN')
        if user and user.is_authenticated:
            cart = user.profile.cart
            cart = cart.unselect_all()
            serializer = self.get_serializer_class()
            return Response(serializer(cart, many=False, context={'user': user, 'currency': currency}).data)
        return Response({'error': 403}, status=403)

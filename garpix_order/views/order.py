from django.conf import settings
from decimal import Decimal
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.permissions import IsOwnerProfileOrReject
from rest_framework.viewsets import ModelViewSet
from ..serializers import OrderSerializer, OrderListSerializer, OrderCreateSerializer, OrderCheckoutSerializer
from ..models import Order, OrderItem, OrderItemCommentPhoto, Collection, CollectionItem
from utils.pagination import CustomPagination
from garpix_catalog.models import Currency, ProductSku, Product
from garpix_cart_rest.models import Cart
from user.models import User, Profile
from datetime import datetime, timedelta


class OrderPagination(CustomPagination):
    pass


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerProfileOrReject, ]
    pagination_class = OrderPagination
    filter_fields = {
        'status': ['exact', ]
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action == 'checkout_order':
            return OrderCheckoutSerializer
        return OrderSerializer

    def get_queryset(self):
        _qs = self.queryset
        if self.request.user.is_authenticated:
            user = self.request.user
            qs = _qs.filter(profile=user.profile).exclude(order_items__isnull=True).exclude(
                status=settings.ORDER_STATUS_UNFORMED)
            #return Response({'error': self.request.data}, status=400)
            if self.request.GET.get('created_at__gte'):
                #return _qs.none()
                data_start1 = self.request.GET.get('created_at__gte')
                date_start = data_start1.split('T')[0][2:]
                date_start = datetime.strptime(date_start, '%y-%m-%d')
                qs = qs.filter(created_at__gte=date_start)

            if self.request.GET.get('created_at__lte'):
                #return _qs.none()
                data_end1 = self.request.GET.get('created_at__lte')
                date_end = data_end1.split('T')[0][2:]
                date_end = datetime.strptime(date_end, '%y-%m-%d') + timedelta(days=1)
                qs = qs.filter(created_at__lte=date_end)



            return qs
        else:
            return _qs.none()

    @action(methods=['GET', ], detail=False)
    def checkout_order(self, request, *args, **kwargs):
        # todo сделать для дропа и опта
        user = request.user
        currency = request.headers.get('currency', 'PLN')
        cart = user.profile.cart
        serializer = self.get_serializer_class()
        checkout_data = serializer(cart, many=False, context={'user': user, 'currency': currency}).data
        checkout_data.update({'total_price': checkout_data['price'] + checkout_data['delivery']['price']})
        return Response(checkout_data)


    @action(methods=['post', ], detail=False)
    def add_comment(self, request, *args, **kwargs):
        try:
            user = request.user
            currency = request.headers.get('currency', 'PLN')
            if user and user.is_authenticated:
                order_id = request.data.get('order_id', None)
                order_item = OrderItem.objects.get(id=order_id)
                try:
                    comment = request.data.get('comment', '')
                    try:
                        order_item.comment = order_item.comment + '_U_' + comment
                    except:
                        order_item.comment = '_U_' + comment
                except:
                    pass
                #try:
                files = request.FILES.getlist('files', [])
                #files = request.FILES
                #return Response({'answer': str(files)})
                #for filename, file in request.FILES.items():
                    #return Response({"error": str(filename)})
                #return Response({"status":str(request.FILES.items()[0])})
                url = ''
                for filename, file in request.FILES.items():
                    try:
                        order_comment_photo = OrderItemCommentPhoto.objects.get(order_item=order_item)
                        order_comment_photo.delete()
                    except:
                        pass
                    file1 = OrderItemCommentPhoto(order_item=order_item, image=file)
                    name = filename
                    file1.save()
                    url = settings.SITE_URL + file1.image.url
                if url == '':
                    try:
                        order_comment_photo = OrderItemCommentPhoto.objects.get(order_item=order_item)
                        url = settings.SITE_URL + order_comment_photo.image.url
                    except:
                        url = ''

                    #orders = OrderItemCommentPhoto.objects.all()
                #return Response({"error": str(request.FILES.items())})

                #except Exception as e:
                    #return Response({"error": str(e)})
                order_item.save()
                return Response({"comment":str(order_item.comment), 'image': url})
        except Exception as e:
            return Response({"error": str(e)})



    """@action(methods=['GET', ], detail=False)
    def get_order_items(self, request, *args, **kwargs):
        try:
            user = request.user
            cart = Cart.objects.filter(profile=user.profile).first()
            order = Order.objects.get(cart=cart, status='unformed')
            return Response({'order': str(order.total_cost)})
        except Exception as e:
            return Response(str(e))"""

    """@action(methods=['post', ], detail=False)
    def filter_by_date(self, request, *args, **kwargs):
        try:
            user = request.user
            data_start1 = request.data.get('date_start', None)
            date_start = data_start1.split('T')[0][2:]
            date_start = datetime.strptime(date_start, '%y-%m-%d')
            date_end1 = request.data.get('date_end', None)
            date_end = date_end1.split('T')[0][2:]
            date_end = datetime.strptime(date_end, '%y-%m-%d')
            orders = Order.objects.filter(profile=user.profile, created_at__range=(date_start, date_end))
            serializer = OrderSerializer(orders)
            return Response(serializer.data, many=True, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)"""

    @action(methods=['post', ], detail=False)
    def delete_order_item(self, request, *args, **kwargs):
        try:
            order_item_id = request.data.get('id', None)
            order_id = request.data.get('order_id', None)
            order = Order.objects.filter(id=order_id).first()
            order_item = order.order_items.filter(id=order_item_id).first()
            #return Response({"status": order_item.status}, status=200)
            if order_item.status == 'paid':
                order.total_cost = order.total_cost - order_item.total_price
                order.save()
                order.profile.balance = order.profile.balance + order_item.total_price
                order.profile.save()
            order_item.delete()
            return Response({"status": "True"}, status=200)
        except Exception as e:
            return Response({"status": "False", "error": str(e)}, status=400)


    @action(methods=['post', ], detail=False)
    def cancel_order_item(self, request, *args, **kwargs):
        order_item_id = request.data.get('id', None)
        order_id = request.data.get('order_id', None)
        order = Order.objects.filter(id=order_id).first()
        order_item = order.order_items.filter(id=order_item_id).first()
        try:
            collection_item = CollectionItem.objects.get(order_item=order_item)
            collection_item.redeemed = False
            collection_item.order_item = None
            #collection_item.collection.status = 0
            collection_item.save()

            collection_item.collection.save()
        except:
            pass
        #return Response({"status": order_item.status}, status=200)
        if order_item.status == 'paid' or order_item.status == 'collection' or order_item.status == 'redeemed':
            order_item_cost = order_item.total_price
            order_cost = order.order_cost
            order.profile.balance = order.profile.balance + order_item.total_price

            order_item.order = None

            order_item.save()
            order.order_cost = order_cost - order_item_cost
            order.save()
            order.profile.save()
        if len(order.order_items.all()) == 0:
            order.status = 'canceled'
            order.save()
        order_item.status = 'canceled'

        order_item.save()
        return Response({"status": "True"}, status=200)

    @action(methods=['post', ], detail=False)
    def delete_order(self, request, *args, **kwargs):
        try:
            order_id = request.data.get('order_id', None)
            order = Order.objects.filter(id=order_id).first()
            if order.status == 'in_process':
                order.profile.balance = order.profile.balance + order.total_cost
                order.profile.save()
            order.delete()
            return Response({"status": "True"}, status=200)
        except Exception as e:
            return Response({"status": "False", "error": str(e)}, status=400)

    @action(methods=['post', ], detail=False)
    def cancel_order(self, request, *args, **kwargs):
        try:
            order_id = request.data.get('order_id', None)
            order = Order.objects.filter(id=order_id).first()
            order_items = order.order_items.all()
            for order_item in order_items:
                try:
                    collection_item = CollectionItem.objects.get(order_item=order_item)
                    collection_item.order_item = None
                    collection_item.save()
                    if collection_item.collection.status == 1:
                        collection_item.collection.status = 0
                        collection_item.collection.save()
                except:
                    pass
                order_item.status = 'canceled'
                order_item.save()
            if order.status == 'in_process':
                order.profile.balance = order.profile.balance + order.total_cost
                order.profile.save()
            order.status = 'canceled'
            order.save()
            return Response({"status": "True"}, status=200)
        except Exception as e:
            return Response({"status": "False", "error": str(e)}, status=400)


    """def list(self, request, *args, **kwargs):
        profile = request.user.profile
        order = profile.user_orders.all()
        serializer = self.get_serializer(order)
        return Response(serializer.data)"""

    def create(self, request, *args, **kwargs):
        profile = request.user.profile
        if request.data.get('add_goods_order_id', None) != 0:

            order_id = request.data.get('add_goods_order_id', None)
            order = Order.objects.get(id=order_id)
            order_old = profile.user_orders.filter(status=settings.ORDER_STATUS_UNFORMED).first()
            order_items = OrderItem.objects.filter(order=order_old)
            for order_item in order_items:
                if profile.balance > order_item.total_price:
                    profile.balance = profile.balance - order_item.total_price
                    profile.save()
                    order_item.status = 'paid'
                else:
                    order_item.status = 'payment_waiting'
                #order.total_cost = order.total_cost + order_item.total_price
                order_item.order = order
                order_item.save()
                order.save()

                if order_item.product.product.product_rc.rc_type == 1:
                    status_collection = False
                    product = order_item.product.product
                    collections = Collection.objects.filter(product=product)
                    if collections.count() > 0:
                        for collection in collections:
                            if status_collection == True:
                                break
                            if collection.product.id == product.id:
                                #collection_items = collection.collection_items
                                collection_items = CollectionItem.objects.filter(collection=collection)
                                for collection_item in collection_items:
                                    if collection_item.sku == order_item.product and collection_item.order_item == None:

                                        if order_item.status == 'payment_waiting':
                                            collection_item.redeemed = False
                                        else:
                                            if not collection_item.order_item:
                                                collection_item.order_item = order_item
                                            collection_item.redeemed = True
                                            # new
                                            if order_item.status != 'collection':
                                                order_item.status = 'collection'
                                                order_item.save()
                                                from user.models import Notification
                                                order_url = settings.SITE_URL_FRONT + order.order_number
                                                url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
                                                notification = Notification(profile=profile1, message='Статус Вашего товара заказа № {0} изменен на {1} '.format(url, settings.ORDER_ITEM_STATUSES[order_item.status]['title']))
                                                notification.save()
                                        collection_item.save()

                                        status_collection = True
                                        break
                    else:
                        collection = Collection(product=product)
                        collection.save()
                        sizes = product.product_rc.sizes.all()
                        for size in sizes:
                            try:
                                product_sku = ProductSku.objects.get(product=product, size=size, color=order_item.product.color)
                            except:
                                product_sku = ProductSku(product=product, size=size, color=order_item.product.color)
                                product_sku.save()
                            collection_item = CollectionItem(collection=collection, sku=product_sku)
                            collection_item.save()
                            if product_sku.id == order_item.product.id:
                                if order_item.status == 'payment_waiting':
                                    collection_item.redeemed = False
                                else:
                                    collection_item.redeemed = True
                                    # new
                                    if order_item.status != 'collection':
                                        order_item.status = 'collection'
                                        order_item.save()
                                        from user.models import Notification
                                        order_url = settings.SITE_URL_FRONT + order.order_number
                                        url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
                                        notification = Notification(profile=profile1, message='Статус Вашего товара заказа № {0} изменен на {1} '.format(url, settings.ORDER_ITEM_STATUSES[order_item.status]['title']))
                                        notification.save()
                                    collection_item.order_item = order_item
                                    collection_item.save()

                                status_collection = True
                                #break
                    if status_collection == False:
                        collection = Collection(product=product)
                        collection.save()
                        sizes = product.product_rc.sizes.all()
                        for size in sizes:
                            try:
                                product_sku = ProductSku.objects.get(product=product, size=size, color=order_item.product.color)
                            except:
                                product_sku = ProductSku(product=product, size=size, color=order_item.product.color)
                                product_sku.save()
                            collection_item = CollectionItem(collection=collection, sku=product_sku)
                            collection_item.save()
                            if product_sku.id == order_item.product.id:
                                if order_item.status == 'payment_waiting':
                                    collection_item.redeemed = False
                                else:
                                    collection_item.redeemed = True
                                    # new
                                    if order_item.status != 'collection':
                                        order_item.status = 'collection'
                                        order_item.save()
                                        from user.models import Notification
                                        order_url = settings.SITE_URL_FRONT + order.order_number
                                        url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
                                        notification = Notification(profile=profile1, message='Статус Вашего товара заказа № {0} изменен на {1} '.format(url, settings.ORDER_ITEM_STATUSES[order_item.status]['title']))
                                        notification.save()
                                    collection_item.order_item = order_item
                                    collection_item.save()

                                status_collection = True
                                #break
            profile.user_orders.filter(status=settings.ORDER_STATUS_UNFORMED).delete()
            order.cart.get_selected_items().update(status=1)
            order.cart.get_selected_packs().update(status=1)

            serializer = self.get_serializer(order)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)
        else:

            order = profile.user_orders.filter(status=settings.ORDER_STATUS_UNFORMED).first()
            amount = Decimal(request.data.get('total_cost', None))
            currency = request.data.get('currency', None)
            if request.data.get('delivery_cost', None):
                if request.data.get('currency', None) == 'PLN':
                    delivery_cost = request.data.get('delivery_cost', None)
                else:
                    delivery_cost = Decimal(request.data.get('delivery_cost', None)) * Decimal(Currency.objects.get(title=currency).ratio)
            else:
                delivery_cost = 0
            Order.objects.filter(id=order.id).update(
                status=settings.ORDER_STATUS_PAYMENT_WAITING,
                comment=request.data.get('comment_order', ''),
                delivery_address=request.data.get('delivery_address', None),
                delivery_method=request.data.get('delivery_method', None),
                payment_method=request.data.get('payment_method', None),
                wait_call=request.data.get('wait_call', False),
                delivery_cost=delivery_cost
            )
            from user.models import Notification
            order_url = settings.SITE_URL_FRONT + order.order_number
            url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
            notification = Notification(profile=order.profile, message='Статус Вашего заказа № {0} изменен на {1} '.format(url, 'Ожидается оплата'))
            notification.save()

            order1 = Order.objects.get(id=order.id)
            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            if int(request.data.get('payment_method', None)) == 3 and order.total_cost<profile.balance:
                Order.objects.filter(id=order.id).update(
                    status=settings.ORDER_STATUS_IN_PROCESS,
                    comment=request.data.get('comment_order', ''),
                    delivery_address=request.data.get('delivery_address', None),
                    delivery_method=request.data.get('delivery_method', None),
                    payment_method=request.data.get('payment_method', None),
                    wait_call=request.data.get('wait_call', False),
                    delivery_cost=delivery_cost
                )
                from user.models import Notification
                order_url = settings.SITE_URL_FRONT + order.order_number
                url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
                notification = Notification(profile=order.profile, message='Статус Вашего заказа № {0} изменен на {1} '.format(url, 'Принят в работу'))
                notification.save()
                user = User.objects.get(id=request.user.id)
                profile1 = Profile.objects.get(user=user)
                if currency != 'PLN':
                    price = amount*Decimal(Currency.objects.get(title=currency).ratio)#get_price_with_currency('USD', amount)
                else:
                    price = amount
                profile1.balance = Decimal(profile1.balance) - price
                profile1.save()
                order = Order.objects.get(id=order.id)
                order_items = OrderItem.objects.filter(order=order)

                for order_item in order_items:
                    # new

                    if order_item.product.product.product_rc.rc_type == 1:
                        status_collection = False
                        product = order_item.product.product
                        collections = Collection.objects.filter(product=product)
                        if collections.count() > 0:
                            for collection in collections:
                                if status_collection == True:
                                    break
                                if collection.product.id == product.id:
                                    collection_items = CollectionItem.objects.filter(collection=collection)
                                    for collection_item in collection_items:
                                        if collection_item.sku == order_item.product and collection_item.order_item == None:

                                            # new
                                            if order_item.status != 'collection':
                                                order_item.status = 'collection'
                                                order_item.save()
                                                from user.models import Notification
                                                order_url = settings.SITE_URL_FRONT + order.order_number
                                                url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
                                                notification = Notification(profile=profile1, message='Статус Вашего товара заказа № {0} изменен на {1} '.format(url, settings.ORDER_ITEM_STATUSES[order_item.status]['title']))
                                                notification.save()
                                            try:
                                                if not collection_item.order_item:
                                                    collection_item.order_item = order_item
                                                collection_item.redeemed = True
                                                collection_item.save()
                                            except:
                                                pass
                                            #if len(collection.collection_items.all().exclude(redeemed=True)) == 0:
                                                #order_item.status = 'redeemed'
                                                #order_item.save()

                                            status_collection = True
                                            break
                        else:
                            product = order_item.product.product
                            collection = Collection(product=product)
                            collection.save()
                            sizes = product.product_rc.sizes.all()

                            for size in sizes:
                                try:
                                    product_sku = ProductSku.objects.get(product=product, size=size, color=order_item.product.color)
                                except:
                                    product_sku = ProductSku(product=product, size=size, color=order_item.product.color)
                                    product_sku.save()
                                collection_item = CollectionItem(collection=collection, sku=product_sku)
                                collection_item.save()
                                if product_sku.id == order_item.product.id:

                                    #return Response({"status": "False", "error": 'ok'}, status=400)
                                    if order_item.status != 'collection':
                                        order_item.status = 'collection'
                                        order_item.save()
                                        from user.models import Notification
                                        order_url = settings.SITE_URL_FRONT + order.order_number
                                        url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
                                        notification = Notification(profile=profile1, message='Статус Вашего товара заказа № {0} изменен на {1} '.format(url, settings.ORDER_ITEM_STATUSES[order_item.status]['title']))
                                        notification.save()
                                    collection_item.redeemed = True
                                    collection_item.order_item = order_item

                                    collection_item.save()

                                    #if len(collection.collection_items.all().exclude(redeemed=True)) == 0:
                                        #order_item.status = 'redeemed'
                                        #order_item.save()
                                    status_collection = True
                                    #break

                        if status_collection == False:
                            collection = Collection(product=product)
                            collection.save()
                            sizes = product.product_rc.sizes.all()
                            for size in sizes:
                                try:
                                    product_sku = ProductSku.objects.get(product=product, size=size, color=order_item.product.color)
                                except:
                                    product_sku = ProductSku(product=product, size=size, color=order_item.product.color)
                                    product_sku.save()
                                collection_item = CollectionItem(collection=collection, sku=product_sku)
                                collection_item.save()
                                if product_sku.id == order_item.product.id:

                                    # new
                                    if order_item.status != 'collection':
                                        order_item.status = 'collection'
                                        order_item.save()
                                        from user.models import Notification
                                        order_url = settings.SITE_URL_FRONT + order.order_number
                                        url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
                                        notification = Notification(profile=profile1, message='Статус Вашего товара заказа № {0} изменен на {1} '.format(url, settings.ORDER_ITEM_STATUSES[order_item.status]['title']))
                                        notification.save()
                                    collection_item.redeemed = True
                                    collection_item.order_item = order_item
                                    collection_item.save()
                                    #if len(collection.collection_items.all().exclude(redeemed=True)) == 0:
                                        #order_item.status = 'redeemed'
                                        #order_item.save()
                                    status_collection = True
                                    #break

                    else:
                        order_item.status = 'paid'
                        order_item.save()
            else:
                order = Order.objects.get(id=order.id)
                order_items = OrderItem.objects.filter(order=order)
                for order_item in order_items:
                    order_items = OrderItem.objects.filter(order=order)
                    """if order_item.product.product.product_rc.rc_type == 1:
                        status_collection = False
                        product = order_item.product.product
                        collections = Collection.objects.filter(product=product)
                        if collections.count() > 0:
                            for collection in collections:
                                if collection.product.id == product.id:
                                    #collection_items = collection.collection_items
                                    collection_items = CollectionItem.objects.filter(collection=collection)
                                    for collection_item in collection_items:
                                        if collection_item.sku == order_item.product and collection_item.order_item == None and status_collection == False:
                                            collection_item.order_item = order_item
                                            collection_item.redeemed = False
                                            collection_item.save()

                                            status_collection = True
                        else:
                            collection = Collection(product=product)
                            collection.save()
                            sizes = product.product_rc.sizes.all()
                            for size in sizes:
                                try:
                                    product_sku = ProductSku.objects.get(product=product, size=size, color=order_item.product.color)
                                except:
                                    product_sku = ProductSku(product=product, size=size, color=order_item.product.color)
                                    product_sku.save()
                                collection_item = CollectionItem(collection=collection, sku=product_sku)
                                collection_item.save()
                                if product_sku.id == order_item.product.id and status_collection == False:
                                    collection_item.redeemed = False
                                    collection_item.order_item = order_item
                                    collection_item.save()
                                    status_collection = True
                        if status_collection == False:
                            collection = Collection(product=product)
                            collection.save()
                            sizes = product.product_rc.sizes.all()
                            for size in sizes:
                                try:
                                    product_sku = ProductSku.objects.get(product=product, size=size, color=order_item.product.color)
                                except:
                                    product_sku = ProductSku(product=product, size=size, color=order_item.product.color)
                                    product_sku.save()
                                collection_item = CollectionItem(collection=collection, sku=product_sku)
                                collection_item.save()
                                if product_sku.id == order_item.product.id:
                                    collection_item.redeemed = False
                                    collection_item.order_item = order_item
                                    collection_item.save()
                                    status_collection = True"""

            order_items = OrderItem.objects.filter(order=order)
            for ss in order.cart.get_selected_items():
                for tt in order_items:
                    if ss.product.id == tt.product.id:
                        try:
                            tt.comment = ss.comment.comment
                            tt.save()
                        except:
                            pass
                        try:
                            tt.change_agreement = ss.change_agreement
                            tt.save()
                        except:
                            pass
            order.cart.get_selected_items().update(status=1)
            order.cart.get_selected_packs().update(status=1)

            serializer = self.get_serializer(order)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)


def get_price_with_currency(currency_title, price):
    try:
        currency = Currency.objects.get(title=currency_title).ratio
    except:
        currency = Decimal('1.0000')
    price = price / currency
    return price.__round__(2)

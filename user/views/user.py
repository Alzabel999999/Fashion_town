from ..models import User
from rest_framework import viewsets
from ..serializers.user import (
    CreateUserSerializer,
    PasswordSerializer,
    UpdateUserSerializer,
    UserSerializer,
    ResetPasswordSerializer,
    UserLoginSerializer,
    UserLoginPhoneSerializer,
    UserLoginEmailSerializer,
    UserNewPhoneSerializer,
    CreateShopUserSerializer,
    ShopUserSerializer,
    ShopUsersListSerializer,
)
from rest_framework.decorators import api_view
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from garpix_utils.strings import get_random_string
from django.conf import settings
from garpix_notify.models import Notify, NotifyCategory
from rest_framework import permissions
from user.permissions import IsUser
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.authtoken.models import Token
#  from django.contrib.auth.base_user import is_authenticated
from utils.pagination import CustomPagination
from garpix_catalog.models import Currency


class ShopUserPagination(CustomPagination):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if self.action == 'update':
            return UpdateUserSerializer
        if self.action == 'partial_update':
            return UpdateUserSerializer
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'login_by_phone':
            return UserLoginPhoneSerializer
        if self.action == 'login_by_email':
            return UserLoginEmailSerializer
        if self.action == 'logout':
            return UserSerializer
        if self.action == 'create_shop_user':
            return CreateShopUserSerializer
        if self.action == 'get_shop_user':
            return ShopUserSerializer
        if self.action == 'get_shop_users_list':
            return ShopUsersListSerializer
        return UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action not in (
                'create',
                'login',
                'login_by_phone',
                'login_by_email',
                'reset_password',
                'create_shop_user',
                'get_shop_user',
                'get_shop_users_list',
        ):
            permission_classes += [permissions.IsAuthenticatedOrReadOnly, IsUser]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_phone = instance.phone
        serializer = self.get_serializer_class()
        data = serializer(instance=instance, data=request.data, partial=True)
        if data.is_valid(raise_exception=True):
            instance = data.save()
            instance.set_profile_data(request.data)
            # email = request.data.get('email', None)
            # user = User.objects.get(pk=request.user.pk)
            # if email and instance.email != email:
            #     user.send_email_confirmation_key(email)
            return Response({'status': True, 'data': data.data})
        return Response({'status': False, 'error': data.errors})

    @action(detail=False, methods=['post'], serializer_class=ResetPasswordSerializer)
    def reset_password(self, request):
        from shop.models import Shop
        data = request.data
        email = data.get('email', None)
        key = data.get('confirm_key', None)
        password = data.get('password', None)
        shop = Shop.get_shop_by_request(request)

        if not email:
            return Response({'status': False, 'message': 'no email'})
        if shop:
            user = shop.get_buyers().filter(email=email).first()
            site_url = shop.site.domain
        else:
            user = User.objects.filter(is_shop_buyer=False, is_buyer=True, email=email).first()
            site_url = settings.SITE_URL
        if not user:
            return Response({'status': False, 'message': 'no user'})
        if not key:
            user.generate_key('password')
            Notify.send(
                event=settings.NOTIFY_EVENT_RESTORE_PASSWORD,
                context={'site': site_url, 'password_reset_key': user.password_reset_key},
                email=email
            )
            return Response({'status': True, 'message': 'confirm key sended'})
        if user.password_reset_key != key:
            return Response({'status': False, 'message': 'wrong confirm key'})
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid():
            user.set_password(password)
            user.save()
            return Response({'status': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=PasswordSerializer)
    def set_password(self, request):
        serializer = PasswordSerializer(data=request.data)
        user = request.user
        if not user.is_authenticated:
            return Response({'non_field': ['Необходимо авторизоваться']}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Неправильный пароль.']}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Получение данных текущего пользователя.
        """
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            # return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': False, 'user': 'AnonymousUser'})

    @action(methods=['post'], detail=False)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_active:
                return Response({'error': 'user was deleted'}, status=400)
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'wrong auth data'}, status=400)

    @action(methods=['post'], detail=False)
    def login_by_phone(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        _user = User.objects.filter(phone=phone).first()
        if _user:
            username = _user.username
            user = authenticate(request, username=username, password=password)
            if user:
                if not user.is_active:
                    return Response({'error': 'user was deleted'}, status=400)
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
        return Response({'error': 'wrong auth data'}, status=400)

    @action(methods=['post'], detail=False)
    def login_by_email(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        _user = User.objects.filter(email=email).first()
        if _user:
            username = _user.username
            user = authenticate(request, username=username, password=password)
            if user:
                if not user.is_active:
                    return Response({'error': 'user was deleted'}, status=400)
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
        return Response({'error': 'wrong auth data'}, status=400)

    @action(methods=['post'], detail=False)
    def logout(self, request):
        token = request.headers.get('Authorization', None)
        if token:
            token = str(token).split(' ')[-1]
            Token.objects.filter(key=token).delete()
        logout(request)
        return Response({})

    @action(methods=['post'], detail=False)
    def set_new_phone(self, request):
        data = request.data
        phone = data.get('phone', None)
        key = data.get('confirm_key', None)

        if not phone:
            return Response({'status': False, 'message': 'no phone'})
        user = request.user
        if not user or not user.is_authenticated:
            return Response({'status': False, 'message': 'no user'})
        if not key:
            user.generate_key('phone')
            # todo: send confirm code
            return Response({'status': True, 'message': 'confirm key sended'})
        if user.phone_change_key != key:
            return Response({'status': False, 'message': 'wrong confirm key'})
        serializer = UserNewPhoneSerializer(data=data)
        if serializer.is_valid():
            user.phone = phone
            user.save()
            return Response({'status': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        user.deactivate_user()
        serializer = self.get_serializer(user)
        logout(request)
        return Response(serializer.data)

    @action(methods=['POST', ], detail=False)
    def create_shop_user(self, request, *args, **kwargs):
        from shop.models import Shop
        shop = Shop.get_shop_by_request(request)
        if not shop:
            return Response(status=400)
        username = request.data.get('username')
        site_username = User.create_buyer_username(username=username, shop_id=shop.id)
        request.data.update({'username': site_username})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET', ], detail=True)
    def get_shop_user(self, request, *args, **kwargs):
        shop = request.user.profile.profile_shop
        if not shop:
            return Response(status=400)
        user = self.get_object()
        if user not in shop.get_buyers():
            return Response(status=400)
        if not user:
            return Response(status=400)
        serializer = self.get_serializer_class()
        return Response(serializer(user).data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def get_user_balance(self, request, *args, **kwargs):
        try:
            balance = request.user.profile.balance
            passive_balance = request.user.profile.passive_balance()
            if passive_balance == None:
                passive_balance = 0
            currency = request.data.get('currency')

            #return Response({"len":str(currency)})
            if currency != 'PLN':
                kurs = Currency.objects.get(title=currency).ratio
                if passive_balance != 0:
                    passive_balance = round(float(passive_balance)/float(kurs),2)
                new_balance = round(float(balance)/float(kurs),2)
            else:

                passive_balance = round(float(passive_balance), 2)
                new_balance = round(float(balance),2)
            return Response({"currency": currency, "balance": new_balance, "passive_balance": passive_balance})
        except Exception as e:
            return Response({"error": str(e)})


    @action(methods=['GET', ], detail=False, pagination_class=ShopUserPagination)
    def get_shop_users_list(self, request, *args, **kwargs):
        shop = request.user.profile.profile_shop
        if not shop:
            return Response(status=400)
        buyers = shop.get_buyers()
        page = self.paginate_queryset(buyers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(buyers, many=True)
        return Response(serializer.data)

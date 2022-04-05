from garpix_page.models import Page
from rest_framework import serializers
from ..models import User
from datetime import datetime
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework.validators import UniqueValidator
from django.conf import settings
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'is_active',
            'username',
            'email',
            'phone',
            'first_name',
            'middle_name',
            'last_name',
        )
        read_only = (
            'username',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    inn = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    vk_link = serializers.SerializerMethodField()
    insta_link = serializers.SerializerMethodField()
    site_link = serializers.SerializerMethodField()
    receive_newsletter = serializers.SerializerMethodField()

    def validate_email(self, value):
        _user = User.objects.filter(email=value).exclude(id=self.instance.id).first()
        if _user is not None:
            raise serializers.ValidationError('Данный E-mail уже используется.')
        return value

    def get_inn(self, obj):
        return obj.profile.inn

    def get_organization(self, obj):
        return obj.profile.organization

    def get_vk_link(self, obj):
        return obj.profile.vk_link

    def get_insta_link(self, obj):
        return obj.profile.insta_link

    def get_site_link(self, obj):
        return obj.profile.site_link

    def get_receive_newsletter(self, obj):
        return obj.profile.receive_newsletter

    class Meta:
        model = User
        fields = (
            'id',
            'is_active',
            'username',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'inn',
            'organization',
            'vk_link',
            'insta_link',
            'site_link',
            'receive_newsletter',
        )
        read_only = (
            'username',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='Email уже используется другим пользователем')]
    )
    phone = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='Телефон уже используется другим пользователем')]
    )

    role = serializers.SerializerMethodField()
    vk_link = serializers.SerializerMethodField()
    insta_link = serializers.SerializerMethodField()
    other_link = serializers.SerializerMethodField()
    inn = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    def get_role(self, obj):
        return obj.profile.role

    def get_vk_link(self, obj):
        return obj.profile.vk_link

    def get_insta_link(self, obj):
        return obj.profile.insta_link

    def get_other_link(self, obj):
        return obj.profile.other_link

    def get_inn(self, obj):
        return obj.profile.inn

    def get_organization(self, obj):
        return obj.profile.organization

    def validate(self, data):
        password = data.get('password', None)
        User(**data)
        errors = dict()
        try:
            if password is not None:
                validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(CreateUserSerializer, self).validate(data)

    def create(self, validated_data):

        request = self.context.get("request")
        # _user = User.objects.filter(email=validated_data['email']).first()
        #
        # if _user is not None:
        #     return Response({
        #         "email": [
        #             "Данный E-mail уже используется. Если вы забыли пароль, попробуйте его восстановить на экране Авторизации."]
        #     }, status=400)

        role = request.data.get('role', 0)
        vk_link = request.data.get('vk_link', None)
        insta_link = request.data.get('insta_link', None)
        other_link = request.data.get('other_link', None)
        inn = request.data.get('inn', None)
        organization = request.data.get('organization', None)
        status = 0

        if role in [2, 3]:
            status = 1
            if vk_link in [None, ''] and insta_link in [None, ''] and other_link in [None, '']:
                errors = {'error': 'Должна быть указана хотя бы одна соцсеть'}
                raise serializers.ValidationError(errors)

        if role == 3:
            if inn in [None, ''] or organization in [None, '']:
                errors = {'error': 'Должны быть указаны ИНН и название организации'}
                raise serializers.ValidationError(errors)

        if role == 1:
            status = 3

        user = User.objects.create(
            phone=validated_data['phone'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            middle_name=validated_data['middle_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            status=status,
            is_buyer=True
        )
        user.set_password(validated_data['password'])
        user.save()
        user.profile.role = role
        user.profile.vk_link = vk_link
        user.profile.insta_link = insta_link
        user.profile.other_link = other_link
        user.profile.inn = inn
        user.profile.organization = organization
        user.profile.save()
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'is_active',
            'username',
            'email',
            'phone',
            'password',
            'first_name',
            'middle_name',
            'last_name',
            'role',
            'vk_link',
            'insta_link',
            'other_link',
            'inn',
            'organization',
        )
        read_only = (
            'username',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class ResetPasswordSerializer(serializers.Serializer):
    confirm_key = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_password(self, value):
        validate_password(value)
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserLoginPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password')


class UserLoginEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserNewPhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='Телефон уже используется другим пользователем')]
    )
    class Meta:
        model = User
        fields = ('phone',)


class CreateShopUserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        password = data.get('password', None)
        User(**data)
        errors = dict()
        try:
            if password is not None:
                validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(CreateShopUserSerializer, self).validate(data)

    def create(self, validated_data):

        status = 3

        user = User.objects.create(
            phone=validated_data['phone'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            middle_name=validated_data['middle_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            status=status,
            is_shop_buyer=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'is_active',
            'username',
            'email',
            'phone',
            'password',
            'first_name',
            'middle_name',
            'last_name',
        )
        read_only = (
            'username',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ShopUserSerializer(serializers.ModelSerializer):

    # todo убрать заглушки
    last_activity = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    balances = serializers.SerializerMethodField()
    orders_count = serializers.SerializerMethodField()

    def get_last_activity(self, obj):
        return datetime.now()

    def get_address(self, obj):
        return 'some address'

    def get_balances(self, obj):
        return {
            'balance': '100',
            'balance_await': '200',
        }

    def get_orders_count(self, obj):
        return '2'
    # -------------

    class Meta:
        model = User
        fields = [
            'id',
            'is_active',
            'username',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone',
            'last_activity',
            'address',
            'balances',
            'orders_count',
        ]


class ShopUsersListSerializer(serializers.ModelSerializer):

    # todo убрать заглушки
    last_activity = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    balances = serializers.SerializerMethodField()

    def get_last_activity(self, obj):
        return datetime.now()

    def get_address(self, obj):
        return 'some address'

    def get_balances(self, obj):
        return {
            'balance': '100',
            'balance_await': '200',
        }
    # -------------

    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.last_name and obj.first_name:
            name = f'{obj.last_name} {obj.first_name[0]}.'
            if obj.middle_name:
                name += f'{obj.middle_name[0]}.'
            return name
        else:
            return obj.username

    def get_url(self, obj):
        return Page.objects.filter(
            page_type=settings.PAGE_TYPE_SHOP_CLIENT_DETAIL).first().get_absolute_url() + f'?client_id={obj.id}'

    class Meta:
        model = User
        fields = [
            'id',
            'is_active',
            'username',
            'url',
            'name',
            'email',
            'phone',
            'date_joined',
            'last_activity',
            'address',
            'balances',
        ]

from django.conf import settings
from rest_framework import serializers
from config.models import SiteConfiguration


class SiteConfigurationSerializer(serializers.ModelSerializer):

    page_type_landing = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_cart = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_account = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_profile = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_auth = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_reg = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_reset_pass = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_checkout = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_order_history = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_wishlist = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_comparsion = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_search = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_catalog = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_news = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_reviews = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_live_photos = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_shop_create = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_404 = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    page_type_500 = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    logo_1 = serializers.SerializerMethodField()
    logo_2 = serializers.SerializerMethodField()
    policy = serializers.SerializerMethodField()
    terms = serializers.SerializerMethodField()
    order_condition = serializers.SerializerMethodField()
    return_rules = serializers.SerializerMethodField()

    def get_logo_1(self, obj):
        return settings.SITE_URL + obj.logo_1.url if obj.logo_1 else '#'

    def get_logo_2(self, obj):
        return settings.SITE_URL + obj.logo_2.url if obj.logo_2 else '#'

    def get_policy(self, obj):
        return settings.SITE_URL + obj.policy.url if obj.policy else '#'

    def get_terms(self, obj):
        return settings.SITE_URL + obj.terms.url if obj.terms else '#'

    def get_order_condition(self, obj):
        return settings.SITE_URL + obj.order_condition.url if obj.order_condition else '#'

    def get_return_rules(self, obj):
        return settings.SITE_URL + obj.return_rules.url if obj.return_rules else '#'

    class Meta:
        model = SiteConfiguration
        fields = [
            'singleton_instance_id', 'logo_1', 'logo_2', 'logo_text',
            'policy', 'terms', 'order_condition', 'return_rules',
            'vk_link', 'insta_link', 'fb_link', 'whatsapp_link', 'telegram_link', 'viber_link',
            'contacts',
            'page_type_landing', 'page_type_cart', 'page_type_account', 'page_type_profile', 'page_type_auth',
            'page_type_reg', 'page_type_reset_pass', 'page_type_checkout', 'page_type_order_history',
            'page_type_wishlist', 'page_type_comparsion', 'page_type_search', 'page_type_catalog', 'page_type_news',
            'page_type_reviews', 'page_type_live_photos', 'page_type_shop_create', 'page_type_404', 'page_type_500',
            'robots_txt', 'scripts',
        ]

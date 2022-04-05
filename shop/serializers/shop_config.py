from rest_framework import serializers
from ..models import ShopConfig
from garpix_order.models import Country


class ShopConfigSerializer(serializers.ModelSerializer):

    contacts_country = serializers.SerializerMethodField()
    footer_country = serializers.SerializerMethodField()

    def get_contacts_country(self, obj):
        return obj.contacts_country.title if obj.contacts_country else ''

    def get_footer_country(self, obj):
        return obj.footer_country.title if obj.footer_country else ''

    class Meta:
        model = ShopConfig
        fields = [
            'main_first_background', 'main_first_text', 'main_banner_1', 'main_banner_2', 'main_banner_3',
            'info_delivery', 'info_payment', 'info_exchange', 'info_juridical',
            'info_delivery_photo', 'info_payment_photo', 'info_exchange_photo', 'info_juridical_photo',
            'about_logo', 'about_photo', 'about_short_description', 'about_full_description',
            'contacts_title', 'contacts_phone', 'contacts_email',
            'contacts_country', 'contacts_city', 'contacts_street', 'contacts_domofon', 'contacts_post_code',
            'contacts_social_vk', 'contacts_social_insta', 'contacts_social_fb', 'contacts_text',
            'footer_logo', 'footer_policy', 'footer_phone', 'footer_email',
            'footer_country', 'footer_city', 'footer_street', 'footer_domofon', 'footer_post_code',
            'footer_social_vk', 'footer_social_insta', 'footer_social_fb',
            'delivery_method_1_title', 'delivery_method_2_title', 'delivery_method_3_title',
            'delivery_method_1_price', 'delivery_method_2_price', 'delivery_method_3_price',
        ]

    def validate(self, attrs):
        data = self.context['request'].data
        contacts_country = data.get('contacts_country', None)
        if contacts_country:
            attrs.update({'contacts_country': Country.objects.filter(id=contacts_country).first()})
        footer_country = data.get('footer_country', None)
        if footer_country:
            attrs.update({'footer_country': Country.objects.filter(id=footer_country).first()})
        return attrs

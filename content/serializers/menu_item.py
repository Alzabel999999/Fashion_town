from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from garpix_menu.models import MenuItem
from ..mixins.serializers import FullImagePathMixin


class MenuItemSerializer(FullImagePathMixin, serializers.ModelSerializer):
    url = serializers.CharField(source='get_link', read_only=True)
    children = RecursiveField(required=False, many=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'title_for_admin', 'title', 'menu_type',
            'page', 'url', 'target_blank', 'css_class', 'edition_style',
            'sort', 'parent', 'children', 'is_only_for_authenticated',
            'is_current', 'is_current_full'
        ]

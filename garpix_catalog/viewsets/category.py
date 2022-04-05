from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ..permissions import IsAdminOrReadOnly
from ..models import Category
from ..serializers.category import CategorySerializer, CategoryListSerializer



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects_with_products.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, )
    filter_fields = {
        'parent': ['isnull', ],
        'title': ['icontains', ],
    }
    ordering_fields = ('title', )

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer

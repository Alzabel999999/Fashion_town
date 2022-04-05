from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from garpix_catalog.models import Product
from django.db.models import Q
from garpix_catalog.serializers import ProductListSerializer


class GlobalSearch(APIView, LimitOffsetPagination):

    default_limit = 30

    def get(self, request):
        if request.method == 'GET':
            q = request.GET.get('q', None)
            if not q:
                return Response({
                    'count': 0,
                    'next': None,
                    'previous': None,
                    'results': []
                })
            q = ' '.join(q.split())
            products = Product.objects.filter(is_active=True).filter(
                Q(title__icontains=q) | Q(content__icontains=q) | Q(vendor_code__icontains=q)).distinct()

            results = self.paginate_queryset(products, request, view=self)
            serializer = ProductListSerializer(results, many=True, context={'user': request.user}).data
            return self.get_paginated_response(serializer)

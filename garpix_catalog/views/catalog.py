from rest_framework import views
from rest_framework.response import Response

from ..serializers import CatalogSerializer
from ..models import Category


class CatalogView(views.APIView):

    def get(self, request):
        data = {
            'categories': CatalogSerializer(Category.objects.filter(parent__isnull=True), many=True).data
        },
        return Response(data)

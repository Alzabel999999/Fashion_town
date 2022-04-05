from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from . import views, viewsets


router = DefaultRouter()

# router.register(r'shop', viewsets.ShopViewSet)
# router.register(r'', viewsets.ShopConfigViewSet)
#
# urlpatterns = router.urls
#
# urlpatterns += [
#     re_path(r'some', viewsets.ShopViewSet.as_view({'get': 'some'}))
# ]

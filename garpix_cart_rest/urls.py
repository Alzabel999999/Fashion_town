from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from . import views


router = DefaultRouter()

router.register(r'', views.CartViewSet)

urlpatterns = router.urls

urlpatterns += [
]

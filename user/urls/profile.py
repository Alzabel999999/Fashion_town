from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .. import views, viewsets
from django.contrib.auth import views as auth_views
from garpix_auth.rest.obtain_auth_token import obtain_auth_token


router = DefaultRouter()
router.register(r'already_saw', viewsets.AlreadySawViewSet)
router.register(r'wishlist', viewsets.WishListViewSet)
router.register(r'notifications', viewsets.NotificationViewSet)

urlpatterns = router.urls

urlpatterns += [
]

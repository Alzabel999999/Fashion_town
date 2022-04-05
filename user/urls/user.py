from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .. import views, viewsets
from django.contrib.auth import views as auth_views
from garpix_auth.rest.obtain_auth_token import obtain_auth_token
router = DefaultRouter()
router.register(r'user', views.UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    re_path(r'^auth/', obtain_auth_token),
    re_path(r'social-auth/', include('rest_framework_social_oauth2.urls')),
    re_path(r'^confirm/', include('garpix_confirm.urls')),
    # re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

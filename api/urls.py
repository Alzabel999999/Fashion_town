from django.urls import include, path, re_path
from api import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v0.0.1',
        description="API for shop",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('content/', include('content.urls')),
    path('catalog/', include('garpix_catalog.urls')),
    path('confirm/', views.ConfirmAPI.as_view()),
    path('cart/', include('garpix_cart_rest.urls')),
    path('order/', include('garpix_order.urls')),
    path('', include('user.urls.user')),
    path('profile/', include('user.urls.profile')),
    path('shop/', include('shop.urls'))
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^confirm/email/(?P<activation_key>[\w-]+)/$', views.ConfirmEmailView.as_view(), name='confirm_email'),
]

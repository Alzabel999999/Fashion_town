from rest_framework.routers import DefaultRouter
from django.urls import path, re_path

from statistic.views import registration_statistic

router = DefaultRouter()
# router.register(r'admin/statistic/statistic/', register_statistic)

urlpatterns = router.urls

urlpatterns += [
]


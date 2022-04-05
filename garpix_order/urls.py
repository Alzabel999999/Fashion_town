from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from . import views


router = DefaultRouter()

router.register(r'delivery_method', views.DeliveryMethodViewSet)
router.register(r'payment_method', views.PaymentMethodViewSet)
router.register(r'delivery_address', views.DeliveryAddressViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'collections', views.CollectionViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'payment_outputs', views.PaymentOutputViewSet)
router.register(r'service', views.ServiceViewSet)
router.register(r'correspondence', views.CorrespondenceItemViewSet)
router.register(r'correspondence_order_item', views.CorrespondenceOrderItemViewSet)
router.register(r'', views.ShopRequisitesViewSet)
router.register(r'withdrawals', views.WithdrawalViewSet)

urlpatterns = router.urls

urlpatterns += [
    re_path(r'get_random_requisites/', views.RequisitesViewSet.as_view({'get': 'get_random_requisites'})),
    re_path(r'requisites/', views.RequisitesViewSet.as_view({'get': 'list'})),
    path("address_search/", views.AddressSearch.as_view(), name="address_search"),
]

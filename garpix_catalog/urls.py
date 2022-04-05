from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from . import views, viewsets


router = DefaultRouter()

router.register(r'category', viewsets.CategoryViewSet)
router.register(r'product', viewsets.ProductViewSet)
router.register(r'live_photo_album', viewsets.LivePhotoAlbumViewSet)
router.register(r'shop_product', viewsets.ShopProductViewSet)
router.register(r'shop_category_markup', viewsets.ShopCategoryMarkupViewSet)
router.register(r'shop_live_photo', viewsets.ShopLivePhotoAlbumViewSet)
#router.register(r'currency_ratio', viewsets.CurrencyViewSet)

urlpatterns = router.urls

urlpatterns += [
    re_path(r'root', views.CatalogView.as_view()),
    re_path(r'brand', viewsets.BrandViewSet.as_view({'get': 'list'})),
    re_path(r'live_photo_feedback', views.feedback, name='feedback')
]

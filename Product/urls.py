from django.urls import path
from rest_framework import routers
from django.urls import path, include
from Product.API.product_apis import ProductViewSet


router = routers.DefaultRouter()
router.register(r'v1', ProductViewSet, basename="product_api_v1")

urlpatterns = [
    path('', include(router.urls)),
    # path('v1/deletefromfavorits/<int:product_id>/', UserDeleteFavorits.as_view(), name="remove_from_favorits")
]

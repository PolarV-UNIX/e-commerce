from django.urls import path
from rest_framework import routers
from django.urls import path, include
from Payment.API.payment_apis import PaymentViewSet

router = routers.DefaultRouter()
router.register(r'v1', PaymentViewSet, basename="payment_gateway")

urlpatterns = [
    path('', include(router.urls)),
]
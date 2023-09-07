from django.urls import path, include
from rest_framework.routers import DefaultRouter
from User.API.user_apis import UserViewSet

router = DefaultRouter()
""" VERSION 1.0 """
router.register(r'v1', UserViewSet, basename='user_api_1.0')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path
from rest_framework import routers, urlpatterns
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'v1', )

urlpatterns = [
    path('', include(router.urls)),
]

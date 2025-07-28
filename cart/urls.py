from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CartItemViewSet

router = DefaultRouter()
router.register(r'', CartItemViewSet, basename='cartitems')


urlpatterns = [
    path('', include(router.urls)),
]

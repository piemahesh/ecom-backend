from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet, CategoryViewSet,AdminProductViewSet

router = DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'my-products', AdminProductViewSet, basename='my-products')  # Admin-only
router.register(r'', ProductViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

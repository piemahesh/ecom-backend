from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderViewSet ,MerchantDashboardStats

router = DefaultRouter()
router.register(r'', OrderViewSet,basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('merchant/dashboard-stats/', MerchantDashboardStats.as_view(), name='merchant-dashboard-stats'),
]

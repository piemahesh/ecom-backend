from rest_framework import viewsets,permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, ProductCreateUpdateSerializer
from .permissions import IsAdminOrOwner
from rest_framework.exceptions import PermissionDenied
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    @swagger_auto_schema(
        operation_description="Create a product with an image upload.",
        request_body=ProductCreateUpdateSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.none()  # fallback
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_staff:  # or use is_admin if available
            raise PermissionDenied("Only admins can add products here.")
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().created_by != self.request.user:
            raise PermissionDenied("You can only update your own products.")
        serializer.save()

    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_admin:
            raise PermissionDenied("Only admins can add products here.")
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().created_by != self.request.user:
            raise PermissionDenied("You can only update your own products.")
        serializer.save()
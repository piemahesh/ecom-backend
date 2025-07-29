from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from cart.models import CartItem
from .serializers import OrderSerializer
from rest_framework.views import APIView
from products.models import Product
from django.db.models import Sum, Count, Q,F


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # ✅
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'detail': 'Cart is empty'}, status=400)

        order = Order.objects.create(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class MerchantDashboardStats(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        merchant = request.user

        # All products owned by this merchant
        products = Product.objects.filter(created_by=merchant)
        product_ids = products.values_list('id', flat=True)

        # Filter OrderItems for this merchant's products
        merchant_items = OrderItem.objects.filter(product__in=product_ids)

        # Total Revenue from shipped/delivered items
        revenue_data = merchant_items.filter(order__status__in=['shipped', 'delivered']) \
            .aggregate(revenue=Sum(F('product__price') * F('quantity')))

        total_revenue = revenue_data['revenue'] or 0

        # Pending Orders = unique orders that have pending items for this merchant
        pending_orders = Order.objects.filter(items__in=merchant_items.filter(order__status='pending')).distinct().count()

        # Total Orders that include this merchant’s items
        total_orders = Order.objects.filter(items__in=merchant_items).distinct().count()

        # Total Products by this merchant
        total_products = products.count()

        return Response({
            "total_revenue": total_revenue,
            "pending_orders": pending_orders,
            "total_orders": total_orders,
            "total_products": total_products,
        })

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        merchant = request.user

        # All products owned by this merchant
        products = Product.objects.filter(created_by=merchant)
        product_ids = products.values_list('id', flat=True)

        # Filter OrderItems for this merchant's products
        merchant_items = OrderItem.objects.filter(product__in=product_ids)

        # Total Revenue from shipped/delivered items
        revenue_data = merchant_items.filter(order__status__in=['shipped', 'delivered']) \
    .aggregate(revenue=Sum(F('product__price') * F('quantity')))

        total_revenue = revenue_data['revenue'] or 0

        # Pending Orders = unique orders that have pending items for this merchant
        pending_orders = Order.objects.filter(items__in=merchant_items.filter(order__status='pending')).distinct().count()

        # Total Orders that include this merchant’s items
        total_orders = Order.objects.filter(items__in=merchant_items).distinct().count()

        # Total Products by this merchant
        total_products = products.count()

        return Response({
            "total_revenue": total_revenue,
            "pending_orders": pending_orders,
            "total_orders": total_orders,
            "total_products": total_products,
        })
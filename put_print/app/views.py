from django.shortcuts import render

from .models import Product

from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from .models import Product, User, Order, OrderItem, Customization
from .forms import ProductForm
from .serializer import UserSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, CustomizationSerializer
from rest_framework.decorators import api_view
from django.http import HttpResponse, Http404
from rest_framework import viewsets, filters
from .models import Color
from .serializer import ColorSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Put&Print API",
        default_version='v1',
        description="API documentation",
    ),
    public=True
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['username', 'email']

    def deactivate(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.is_active = False
        instance = instance.save()
        return Response({"message": "The User instance is successfully deactivated"})

    def activate(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance = instance.save()
        return Response({"message": "The user is successfully activated"}, status=200)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_id'

    def deactivate(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_available = False
        instance = instance.save()
        return Response({"message": "The product instance is succeffuly deactivated"}, status=200)

    def activate(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_available = True
        instance = instance.save()
        return Response({"message": "The product instance is successfully activated"}, status=200)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'

    @action(detail=True, methods=['get'])
    def orderitems(self, request, order_id=None):
        order = self.get_object()
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True, context={'request': request})
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'orderitem_id'

    def perform_create(self, serializer):
        instance = serializer.save()

        order = instance.order
        order.total_price = order.total_price + instance.total_price
        order.save()
        serializer.save()



class CustomizationViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer
    lookup_field = 'customization_id'
    def validate(self, data):
        if data.get('asset_type') == 'text':
            if not data.get('font_name'):
                raise serializers.ValidationError({"font_name": "This field is required."})
            if not data.get('font_size'):
                raise serializers.ValidationError({"font_size": "This field is required."})
            if not data.get('font_color'):
                raise serializers.ValidationError({"font_color": "This field is required."})
        return data
    
    @action(detail=True, methods=['post'], url_path='create_customization')
    def create_customization(self, request, customization_id=None):
        serializer = CustomizationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            customization = serializer.save()
            order_item = self.get_object()
            
            customization.order_item = order_item
            customization.save()
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    lookup_field = 'color_id'



from rest_framework.routers import DefaultRouter
from app.views import UserViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, CustomizationViewSet, ColorViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename = 'order')
router.register(r'orderitems', OrderItemViewSet, basename = 'orderitem')
router.register(r'customizations', CustomizationViewSet, basename = 'customization')
router.register(r'colors', ColorViewSet, basename = 'color')
from django.urls import path, include
from app.routers import router
from app.views import UserViewSet, ProductViewSet, ColorViewSet, OrderViewSet, schema_view, OrderItemViewSet, CustomizationViewSet

urlpatterns = [
     # User activation and deactivation routes
     path('users/<uuid:user_id>/activate',
     UserViewSet.as_view({"get": "activate"}), name='user-activate'),
     path('users/<uuid:user_id>/deactivate',
     UserViewSet.as_view({"get": "deactivate"}), name='user-deactivate'),

     # Product activation and deactivation routes
     path('products/<uuid:product_id>/activate',
     ProductViewSet.as_view({"get": "activate"}), name='product-activate'),
     path('products/<uuid:product_id>/deactivate',
     ProductViewSet.as_view({"get": "deactivate"}), name='product-deactivate'),

     # OrderItem routes
     path('orders/<uuid:order_id>/items', OrderViewSet.as_view({"get": "orderitems"}), name='order-items'),
     # Include the rest of the API routes via router
     path('', include(router.urls)),
     # Swagger API documentation
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
     # OrderItem creation route
     path('orders/<uuid:order_id>/create_item', OrderItemViewSet.as_view({"post": "create"}), name='orderitem-create'),
     # OrderItem customization route
     path('orderitems/<uuid:item_id>/customization', CustomizationViewSet.as_view({"post": "create_customization"}), name='orderitem-customize')
]

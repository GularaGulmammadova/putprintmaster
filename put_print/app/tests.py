from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Product, Order, OrderItem, Customization, Color


class UserViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', phone='123456789')

    def test_create_user(self):
        response = self.client.post('/api/users/', {'username': 'newuser', 'email': 'new@example.com', 'phone': '987654321'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deactivate_user(self):
        response = self.client.post(f'/api/users/{self.user.user_id}/deactivate/')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(f'/api/users/{self.user.user_id}/activate/')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', phone='123456789')
        self.product = Product.objects.create(name='Sample Product', price=100, user=self.user, type='TSHIRT')

    def test_create_product(self):
        response = self.client.post('/api/products/', {'name': 'New Product', 'price': 150, 'user': self.user.user_id, 'type': 'CAP'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deactivate_product(self):
        response = self.client.post(f'/api/products/{self.product.product_id}/deactivate/')
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_available)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_product(self):
        self.product.is_available = False
        self.product.save()
        response = self.client.post(f'/api/products/{self.product.product_id}/activate/')
        self.product.refresh_from_db()
        self.assertTrue(self.product.is_available)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', phone='123456789')
        self.order = Order.objects.create(user=self.user, total_price=200, shipping_address="Test Address")

    def test_create_order(self):
        response = self.client.post('/api/orders/', {'user': self.user.user_id, 'total_price': 300, 'shipping_address': "New Address"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderItemViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', phone='123456789')
        self.product = Product.objects.create(name='Sample Product', price=100, user=self.user, type='TSHIRT')
        self.order = Order.objects.create(user=self.user, total_price=200, shipping_address="Test Address")
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_create_order_item(self):
        response = self.client.post('/api/orderitems/', {'order': self.order.order_id, 'product': self.product.product_id, 'quantity': 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_total_price_update(self):
        response = self.client.post('/api/orderitems/', {'order': self.order.order_id, 'product': self.product.product_id, 'quantity': 3})
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, 300)


class CustomizationViewSetTests(APITestCase):

    def setUp(self):
        self.customization = Customization.objects.create(name='Sample Customization', asset_type='Type1')

    def test_create_customization(self):
        response = self.client.post('/api/customizations/', {'name': 'New Customization', 'asset_type': 'Type2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ColorViewSetTests(APITestCase):

    def setUp(self):
        self.customization = Customization.objects.create(name='Sample Customization', asset_type='Type1')
        self.color = Color.objects.create(customization=self.customization, fill_color='#FF0000', border_color='#000000', opacity=1.0, gradient_start='#FFFFFF', gradient_end='#000000')

    def test_create_color(self):
        response = self.client.post('/api/colors/', {
            'customization': self.customization.customization_id,
            'fill_color': '#00FF00',
            'border_color': '#0000FF',
            'opacity': 0.8,
            'gradient_start': '#FF0000',
            'gradient_end': '#00FF00'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deactivate_color(self):
        response = self.client.post(f'/api/colors/{self.color.color_id}/deactivate/')
        self.color.refresh_from_db()
        self.assertFalse(self.color.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_color(self):
        self.color.is_active = False
        self.color.save()
        response = self.client.post(f'/api/colors/{self.color.color_id}/activate/')
        self.color.refresh_from_db()
        self.assertTrue(self.color.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

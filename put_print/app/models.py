from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from app.managers import CustomUserManager


class User(AbstractBaseUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255, null=True, blank=True)
    profile_img = models.ImageField(
        upload_to='profile_images/', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()


class Product(models.Model):
    PRODUCT_TYPES = (
        ('TSHIRT', 'T-shirt'),
        ('PANTS', 'Pants'),
        ('CAP', 'Cap'),
    )
    product_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=PRODUCT_TYPES)
    product_image = models.ImageField(
        upload_to='product_images/', max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'

    order_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItem")
    shipping_address = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    orderitem_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    individual_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.individual_price = self.product.price
        self.total_price = self.product.price * self.quantity
        return super().save(*args, **kwargs)


class Customization(models.Model):
    customization_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=255, null=True)
    ASSET_TYPES = (
        ('TEXT', 'Text'),
        ('IMAGE', 'Image'),
    )
    asset_type = models.CharField(max_length=5, choices=ASSET_TYPES)
    font_name = models.CharField(max_length=20, null=True)
    font_size = models.IntegerField(null=True)
    font_color = models.CharField(max_length=7, null=True)
    position_x = models.IntegerField(null=True)
    position_y = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    z_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE)


class Color(models.Model):
    color_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    customization = models.OneToOneField(
        Customization, on_delete=models.SET_NULL, null=True)
    fill_color = models.CharField(max_length=7)
    border_color = models.CharField(max_length=7)
    opacity = models.DecimalField(max_digits=3, decimal_places=2)
    gradient_start = models.CharField(max_length=7)
    gradient_end = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

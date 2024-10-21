from rest_framework import serializers
from .models import User, Product, Order, OrderItem, Customization
from django.core.serializers import serialize
from rest_framework import serializers
from .models import Color





class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='user_id',
        read_only=True
    )

    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'updated_at' in self.initial_data and 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {
                    "updated_at": "You cannot update the update date.",
                    "created_at": "You can not update the creation date"
                })
        elif 'updated_at' in self.initial_data:
            raise serializers.ValidationError(
                {"updated_date": "You cannot update the published date."})
        elif 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {"created_at": "You can not update the creation date"})

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.location = validated_data.get("location", instance.location)
        instance.profile_img = validated_data.get(
            "profile_img", instance.profile_img)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='product_id',
        read_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'updated_at' in self.initial_data and 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {
                    "updated_at": "You cannot update the update date.",
                    "created_at": "You can not update the creation date"
                })
        elif 'updated_at' in self.initial_data:
            raise serializers.ValidationError(
                {"updated_date": "You cannot update the published date."})
        elif 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {"created_at": "You can not update the creation date"})

        instance.type = validated_data.get('type', instance.type)
        instance.product_image = validated_data.get(
            'product_image', instance.product_image)
        instance.price = (validated_data.get('price'), instance.price)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='order-detail',
        lookup_field='order_id',
        read_only=True
    )

    class Meta:
        model = Order
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'updated_at' in self.initial_data and 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {
                    "updated_at": "You cannot update the update date.",
                    "created_at": "You can not update the creation date"
                })
        elif 'updated_at' in self.initial_data:
            raise serializers.ValidationError(
                {"updated_date": "You cannot update the published date."})
        elif 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {"created_at": "You can not update the creation date"})
        instance.shipping_address = validated_data.get(
            'shipping_address', instance.shipping_address)
        instance.status = validated_data.get('status', instance.status)
        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='orderitem-detail',
        lookup_field='orderitem_id',
        read_only=True
    )
    individual_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)

    def update(self, instance, validated_data):
        if 'updated_at' in self.initial_data and 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {
                    "updated_at": "You cannot update the update date.",
                    "created_at": "You cannot update the creation date"
                })
        elif 'updated_at' in self.initial_data:
            raise serializers.ValidationError(
                {"updated_date": "You cannot update the update date."})
        elif 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {"created_at": "You cannot update the creation date"})
        instance.quantity = validated_data.get(
            'quantity', instance.quantity)
        return instance

    class Meta:
        model = OrderItem
        fields = '__all__'


class CustomizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customization
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_id', 'customization', 'fill_color', 'border_color', 'opacity', 
                  'gradient_start', 'gradient_end', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        if 'updated_at' in self.initial_data and 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {
                    "updated_at": "You cannot update the update date.",
                    "created_at": "You cannot update the creation date"
                })
        elif 'updated_at' in self.initial_data:
            raise serializers.ValidationError(
                {"updated_date": "You cannot update the update date."})
        elif 'created_at' in self.initial_data:
            raise serializers.ValidationError(
                {"created_at": "You cannot update the creation date"})
        instance.customization = validated_data.get(
            'customization', instance.customization)
        return instance
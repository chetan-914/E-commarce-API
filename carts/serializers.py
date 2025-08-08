from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    def validate_product_id(self, value):
        from products.models import Product
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product with this ID.")
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance
    
    class Meta:
        model = CartItem
        fields = ('id', 'product_id', 'quantity')

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'total_price')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField()

    def get_total_cart_price(self, cart: Cart):
        return sum(item.total_price for item in cart.items.all())
    
    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_cart_price')
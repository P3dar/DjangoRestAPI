from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategoySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    unit_price = serializers.SerializerMethodField(method_name='get_price')
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')
    name = serializers.SerializerMethodField(method_name='get_name')

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('user', 'unit_price', 'total_price', 'name')

    def get_total_price(self, cart_item: Cart):
        menu_item = cart_item.menuitem
        return cart_item.quantity * menu_item.price

    def get_price(self, cart_item: Cart):
        menu_item = cart_item.menuitem
        return menu_item.price

    def get_name(self, cart_item: Cart):
        menu_item = cart_item.menuitem
        return menu_item.title


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('menuitem', 'quantity', 'unit_price', 'price')


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(
        many=True, read_only=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew',
                  'status', 'total', 'date', 'orderItems')
        read_only_fields = ('user', 'delivery_crew',
                            'status', 'total', 'date', 'orderItems')


class SingleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

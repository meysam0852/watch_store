from rest_framework import serializers
from .models import Product, ProductImage, ProductColor, Comment, Customer, WishList

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'color', 'hex_code']


class CommentSerializer(serializers.ModelSerializer):
    customer_phone = serializers.CharField(source='customer.phone_number', read_only=True)
    author = serializers.CharField(source='customer.user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'customer_phone', 'body', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='brand.name', read_only=True)
    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'brand', 'category', 'is_available', 'stash']


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='brand.name', read_only=True)
    category = serializers.CharField(source='category.title', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class LuxurySpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'gender', 'strap_matterial', 'engine']


class WishListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'price', 'stash', 'main_image']


class WishListCustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number']


class WishListSerializer(serializers.ModelSerializer):
    product = WishListProductSerializer(read_only=True)
    customer = WishListCustomerSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = ['id', 'product', 'customer']
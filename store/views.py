from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, F
from django.shortcuts import get_object_or_404

from .models import Product, WishList
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    LuxurySpecialSerializer,
    WishListSerializer
)

class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.select_related('brand', 'category').all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailAPIView(APIView):
    def get(self, request, slug):
        Product.objects.filter(slug=slug).update(click_count=F('click_count') + 1)
        
        product = get_object_or_404(
            Product.objects.select_related('brand', 'category')
                           .prefetch_related('images', 'colors', 'comments__customer__user'),
            slug=slug
        )

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LuxurySpecialAPIView(APIView):
    def get(self, request):
        luxury_products = Product.objects.filter(
            is_special=True,
            is_luxury=True,
            is_available=True
        )

        avg_calc = Product.objects.filter(is_luxury=True).aggregate(avg_price=Avg('price'))
        avg_price = avg_calc['avg_price']

        serializer = LuxurySpecialSerializer(luxury_products, many=True)
        return Response({
            'average_luxury_price': avg_price,
            'products': serializer.data
        }, status=status.HTTP_200_OK)


class MyWishListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist_items = WishList.objects.filter(customer__user=request.user)\
                                         .select_related('product', 'customer__user')

        serializer = WishListSerializer(wishlist_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

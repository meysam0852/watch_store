from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    LuxurySpecialAPIView,
    MyWishListAPIView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('luxury-special/', LuxurySpecialAPIView.as_view(), name='luxury-special'),
    path('me/wishlist/', MyWishListAPIView.as_view(), name='my-wishlist'),
]
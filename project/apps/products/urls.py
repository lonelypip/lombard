from django.urls import path
from .views import Home, Products, ProductDetail, CategoryDetail, ProductsOwn



urlpatterns = [
    path('', Home.as_view(), name='home_url'),
    path('products/', Products.as_view(), name='products_url'),
    path('products/own/', ProductsOwn.as_view(), name='products_own_url'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail_url'),
    path('products/<str:slug>/', CategoryDetail.as_view(), name='category_detail_url'),
]

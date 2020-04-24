from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Product, Category






class Home(View):
    def get(self, request):
        offers = Product.objects.filter(status=1, offer=True)
        return render(request, 'products/index.html', {'offers':offers})


class Products(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.filter(status=1, offer=False)
        return render(request, 'products/products.html', {
            'products':products,
            'categories':categories
        })


class ProductDetail(View):
    def get(self, request, pk):
        try:
            if Product.objects.get(pk=pk).status == 1:
                product = Product.objects.get(pk=pk)
            else:
                product = None
        except Product.DoesNotExist:
            product = None
        return render(request, 'products/product-detail.html', {'product':product})


class CategoryDetail(View):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
            products = Product.objects.filter(status=1, category=category)
        except Category.DoesNotExist:
            products = None
            category = None
        categories = Category.objects.all()
        return render(request, 'products/category-detail.html', {
            'products':products,
            'category':category,
            'categories':categories
        })


class ProductsOwn(View):
    def get(self, request):
        return render(request, 'products/buyback.html')
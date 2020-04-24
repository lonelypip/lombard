from django.contrib import admin
from .models import Product, Percent, Delay, Category, Check


admin.site.register(Category)
admin.site.register(Percent)
admin.site.register(Delay)
admin.site.register(Product)
admin.site.register(Check)

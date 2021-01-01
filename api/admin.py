from django.contrib import admin

# Register your models here.
from .models import CustomUser, Category, ProductModel, Cart, Products
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ProductModel)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Products)
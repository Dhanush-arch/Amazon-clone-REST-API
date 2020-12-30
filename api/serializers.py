from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('userName', )

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.ProductModel
    fields = "__all__"

class ProductsSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Products
    fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Cart
    fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Category
    fields = '__all__'
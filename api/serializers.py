from rest_framework import serializers
from . import models
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = "__all__"

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

class UseridSerializer(serializers.ModelSerializer):
  class Meta:
    model = Token
    fields = '__all__'

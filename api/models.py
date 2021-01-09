from django.db import models
from django.contrib.auth.models import User as defaultUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(models.Model):
    userName = models.OneToOneField(defaultUser, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.userName.email)


@receiver(post_save, sender=defaultUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(userName=instance, email=instance.email)

# @receiver(post_save, sender=defaultUser)
# def save_user(sender, instance, **kwargs):
#     print(instance)
#     instance.user.save()


class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    productID = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=200, null=True, blank=True )
    productDescription = models.CharField(max_length=1000, null=True, blank=True)
    productPrice = models.FloatField(null=True, blank=True)
    stars = models.IntegerField(null=True, blank=True)
    productImage = models.ImageField(
        upload_to="productImages", null=True, blank=True)
    productCategory = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.productName


class Products(models.Model):
    productsId = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser, verbose_name="user", on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        ProductModel, verbose_name="product", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    ordered = models.BooleanField(default=False, null=True, blank=True)

class Cart(models.Model):
    cartId = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser, verbose_name="user", on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, verbose_name="products")
    price = models.FloatField(null=True, blank=True)
    paymentMethod = models.CharField(max_length=10, null=True, blank=True)
    paymentDone = models.BooleanField(default=False, null=True, blank=True)

    def getTotalPrice(self):
        total = 0
        for pro in self.products.objects.all():
            total = total + pro.product.productPrice * pro.quantity
        return total

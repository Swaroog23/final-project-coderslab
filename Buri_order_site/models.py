from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model


class Ingredients(models.Model):
    name = models.CharField(max_length=150)
    is_gluten = models.BooleanField()
    is_not_vegan = models.BooleanField(default=True)
    is_allergic = models.BooleanField()


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=150)
    street_number = models.IntegerField()
    house_number = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    categories = models.ManyToManyField("Category", related_name="products")
    ingredients = models.ManyToManyField("Ingredients", related_name="products")
    details = models.TextField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ManyToManyField(Product, through="CartProduct")
    cost = models.DecimalField(max_digits=6, decimal_places=2)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=64)
    details = models.TextField()

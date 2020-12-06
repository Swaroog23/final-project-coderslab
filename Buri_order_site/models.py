from django.db import models
from django.contrib.auth.models import User


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name="cart")
    cost = models.DecimalField(max_digits=6, decimal_places=2)


class Category(models.Model):
    name = models.CharField(max_length=64)
    details = models.TextField()

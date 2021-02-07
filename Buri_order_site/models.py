from django.db import models
from django.contrib.auth.models import User


class Ingredients(models.Model):
    name = models.CharField(max_length=150)
    is_gluten = models.BooleanField()
    is_not_vegan = models.BooleanField(default=True)
    is_allergic = models.BooleanField()

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=150)
    street_number = models.IntegerField()
    house_number = models.IntegerField()

    def __str__(self):
        return f"ul.{self.street} {self.street_number}/{self.house_number}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    categories = models.ManyToManyField("Category", related_name="products")
    ingredients = models.ManyToManyField("Ingredients", related_name="products")
    details = models.TextField()

    @staticmethod
    def get_products_and_amounts_from_list(product_list):
        list_of_objects = []
        for item in product_list:
            list_of_objects.append((Product.objects.get(pk=item[0]), item[1]))
        return list_of_objects


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ManyToManyField(Product, through="CartProduct")
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def clear_session(self, request):
        for item in request.session["cart_products"]:
            request.session.pop(item[0])
        request.session.pop("cost")


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=64)
    details = models.TextField()

    def __str__(self):
        return self.name

from Buri_order_site.models import Category, Ingredients, Product
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User


def main_page_view(request):
    return render(request, "main.html")


def category_view(request):
    categories = Category.objects.all()
    return render(request, "categories.html", {"categories": categories})


class CategoryDetailView(View):
    def get(self, request, id):
        category = Category.objects.get(id=id)
        products = Product.objects.filter(categories=category)
        ctx = {"products": products}
        return render(request, "category_detail.html", ctx)
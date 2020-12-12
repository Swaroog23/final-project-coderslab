from Buri_order_site.models import Category
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User


def main_page_view(request):
    return render(request, "main.html")


def category_view(request):
    categories = Category.objects.all()
    return render(request, "categories.html", {"categories": categories})
from django.http.response import HttpResponse
from Buri_order_site.models import Category, Product, Cart
from Buri_order_site.forms import ChangeUserData
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
import json


def main_page_view(request):
    return render(request, "main.html")


def category_view(request):
    return render(request, "categories.html")


class CategoryDetailView(View):
    def get(self, request, id):
        category = Category.objects.get(id=id)
        products = Product.objects.filter(categories=category)
        ctx = {"products": products, "chosen_category": category}
        return render(request, "category_detail.html", ctx)

    def post(self, request, id):
        response = redirect(to=f"/categories/{id}")
        product_in_cart_id = request.POST.get("cart_product")
        product_in_cart_amount = request.POST.get("amount_of_product")
        response.set_cookie(
            key=f"product_{product_in_cart_id}_and_amount",
            value=json.dumps({f"{product_in_cart_id}": f"{product_in_cart_amount}"}),
        )
        return response


class UserSettingsView(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        form = ChangeUserData(initial=user_data)
        ctx = {"form": form}
        return render(request, "change_user_data.html", ctx)

    def post(self, request, user_id):
        form = ChangeUserData(request.POST)
        user = User.objects.get(id=user_id)
        if form.is_valid():
            user.username = form.cleaned_data["username"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            return render(request, "main.html")
        ctx = {"form": form}
        return render(request, "change_user_data.html", ctx)


class CartView(View):
    def get_products_from_json(product_list):
        list_of_product_objects = []
        for json_item in product_list:
            for product_id, amount in json_item.items():
                product_from_db = Product.objects.get(pk=int(product_id))
                list_of_product_objects.append((product_from_db, int(amount)))
        return list_of_product_objects

    def get_products_cost_from_list(product_list):
        total_cost = 0
        for item in product_list:
            total_cost += item[0].price
        return total_cost

    def get(self, request, user_id):
        cookies = request.COOKIES.items()
        products_from_cookies_list = []
        for cookie_name, cookie_value in cookies:
            if "product" and "amount" in cookie_name:
                products_from_cookies_list.append(json.loads(cookie_value))
        list_of_products_in_cart = CartView.get_products_from_json(
            products_from_cookies_list
        )
        cost_of_products = CartView.get_products_cost_from_list(
            list_of_products_in_cart
        )
        ctx = {"chosen_products": list_of_products_in_cart, "cost": cost_of_products}
        return render(request, "cart.html", ctx)
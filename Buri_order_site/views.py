from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from Buri_order_site.models import Category, Product, Cart, CartProduct, Address
from Buri_order_site.forms import (
    AddProductForm,
    ChangeUserData,
    UserAddressForm,
)

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
        try:
            if 10 > int(product_in_cart_amount) > 0:
                response.set_cookie(
                    key=f"product_{product_in_cart_id}_and_amount",
                    value=json.dumps(
                        {f"{product_in_cart_id}": f"{product_in_cart_amount}"}
                    ),
                )
            else:
                messages.error(
                    request, "Błąd dodawania produktu do koszyka, spróbuj ponownie!"
                )
        except (TypeError, ValueError):
            messages.error(
                request, "Błąd dodawania produktu do koszyka, spróbuj ponownie!"
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
        ctx = {"form": form, "logged_user": user}
        return render(request, "change_user_data.html", ctx)

    def post(self, request, user_id):
        form = ChangeUserData(request.POST)
        user = User.objects.get(id=user_id)
        ctx = {"form": form, "logged_user": user}
        if form.is_valid():
            user.username = form.cleaned_data["username"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            ctx["info"] = "Pomyślnie zmieniono dane!"
            return render(request, "change_user_data.html", ctx)
        ctx["info"] = "Wystąpił błąd"
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
            total_cost = total_cost + (item[0].price * item[1])
        return total_cost

    def get(self, request, user_id):
        cookies = request.COOKIES.items()
        products_from_cookies_list = []
        for cookie_name, cookie_value in cookies:
            if "product" and "amount" in cookie_name:
                products_from_cookies_list.append(json.loads(cookie_value))
        list_of_products_in_cart_with_amount = CartView.get_products_from_json(
            products_from_cookies_list
        )
        cost_of_products = CartView.get_products_cost_from_list(
            list_of_products_in_cart_with_amount
        )
        request.session["products_ids_and_amount"] = products_from_cookies_list
        ctx = {
            "chosen_products": list_of_products_in_cart_with_amount,
            "cost": cost_of_products,
        }
        return render(request, "cart.html", ctx)

    def post(self, request, user_id):
        cookie_to_delete = request.POST.get("delete-btn")
        response = redirect(f"/cart/{user_id}/")
        response.delete_cookie(cookie_to_delete)
        return response


class PaymentView(View):

    TOTAL_COST_FOR_ORDER = 0
    LIST_OF_ORDERD_PRODUCTS = []

    def get(self, request, user_id):
        list_of_products_ids_and_amount = request.session.get("products_ids_and_amount")
        form = UserAddressForm()
        list_of_products_models_with_amount = CartView.get_products_from_json(
            list_of_products_ids_and_amount
        )
        total_cost_of_order = CartView.get_products_cost_from_list(
            list_of_products_models_with_amount
        )
        PaymentView.TOTAL_COST_FOR_ORDER = total_cost_of_order
        PaymentView.LIST_OF_ORDERD_PRODUCTS = list_of_products_models_with_amount
        ctx = {
            "chosen_products": list_of_products_models_with_amount,
            "cost": total_cost_of_order,
            "form": form,
        }
        return render(request, "payment.html", ctx)

    def post(self, request, user_id):
        if user_id != "None":
            form = UserAddressForm(request.POST)
            user = User.objects.get(pk=user_id)
            cart = Cart.objects.create(user=user, cost=0)
            if form.is_valid():
                user_address_street = form.cleaned_data["street"]
                user_address_street_num = form.cleaned_data["street_number"]
                user_address_house_num = form.cleaned_data["house_number"]
                user.address_set.get_or_create(
                    street=user_address_street,
                    street_number=user_address_street_num,
                    house_number=user_address_house_num,
                )
        cart = Cart.objects.create(cost=0)
        for product, amount in PaymentView.LIST_OF_ORDERD_PRODUCTS:
            cart.cost += product.price * amount
            CartProduct.objects.create(cart=cart, product=product, amount=amount)
        cart.save()
        response = render(request, "main.html", {"info": "Zamówienie złożone!"})
        for cookie_name, cookie_value in request.COOKIES.items():
            if "product" and "amount" in cookie_name:
                response.delete_cookie(cookie_name)

        return response


class CreateNewUserView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "create_user.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data["username"])
            login(request, user)
            return render(request, "main.html", {"info": "Utworzono użytkownika!"})
        return render(
            request,
            "create_user.html",
            {"info": "Wystąpił błąd, spróbuj ponownie.", "form": UserCreationForm()},
        )


class AdminAddProductView(View):
    def get(self, request):
        form = AddProductForm()
        return render(request, "add_product.html", {"form": form})

    def post(self, request):
        form = AddProductForm(request.POST)
        if form.is_valid():
            chosen_ingredients = form.cleaned_data["ingredients"]
            chosen_categories = form.cleaned_data["categories"]
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            details = form.cleaned_data["details"]
            new_product = Product.objects.create(
                name=name,
                price=price,
                details=details,
            )
            new_product.categories.set(chosen_categories)
            new_product.ingredients.set(chosen_ingredients)
            new_product.save()
            return render(
                request,
                "add_product.html",
                {"info": "Produkt dodano!", "form": AddProductForm()},
            )
        return render(
            request,
            "add_product.html",
            {"form": AddProductForm(), "info": "Niepoprawne dane, spróbuj ponownie"},
        )


class UserAddNewAddress(View):
    def get(self, request, user_id):
        form = UserAddressForm()
        return render(request, "user_add_new_address.html", {"form": form})

    def post(self, request, user_id):
        form = UserAddressForm(request.POST)
        user = User.objects.get(pk=user_id)
        ctx = {"form": form}
        if form.is_valid():
            street = form.cleaned_data["street"]
            stret_number = form.cleaned_data["street_number"]
            house_number = form.cleaned_data["house_number"]
            try:
                address = Address.objects.get(
                    user=user,
                    street=street,
                    street_number=stret_number,
                    house_number=house_number,
                )
                if address in user.address_set.all():
                    ctx["info"] = "Podany adres jest już zapisany!"
                    return render(request, "user_add_new_address.html", ctx)
            except ObjectDoesNotExist:
                user.address_set.add(
                    Address.objects.create(
                        user=user,
                        street=street,
                        street_number=stret_number,
                        house_number=house_number,
                    )
                )
                ctx["info"] = "Pomyślnie dodano adres dostawy!"
                return render(request, "user_add_new_address.html", ctx)
        return render(request, "user_add_new_address.html", ctx)

from Buri_order_site.models import Category, Product, Cart
from Buri_order_site.forms import ChangeUserData

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User


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
        product_in_cart_id = f"{request.POST.get('cart_product')}"
        product_in_cart_amount = f"{request.POST.get('amount_of_product')}"
        response.set_cookie(
            key=f"product_{product_in_cart_id}_and_amount",
            value={product_in_cart_id: product_in_cart_amount},
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


# class CartView(View):
#     def get(self, request, user_id):
#         if user_id == "None":
#             pass
#         else:
#             return HttpResponse("DUPA")
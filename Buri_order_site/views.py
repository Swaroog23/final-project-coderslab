from django.contrib.auth.forms import UserCreationForm
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
    UserOldAddressForm,
    ChangeUsernameForm,
)

import json


def main_page_view(request):
    return render(request, "main.html")


def category_view(request):
    """List of category objects is taken from context_processor.py"""

    return render(request, "categories.html")


class CategoryDetailView(View):
    """View returning products and their details from their category."""

    def get(self, request, id):
        """Method for GET request.

        Args:
            id (int): id value of Category model

        Returns:
            List of products from category
        """
        category = Category.objects.get(id=id)
        products = Product.objects.filter(categories=category)
        ctx = {"products": products, "chosen_category": category}
        return render(request, "category_detail.html", ctx)

    def post(self, request, id):
        """Method for POST request, sent by forms under each product.

        Args:
            id (int): id value of Category model.

        Returns:
            Redirect response to same site with cookies containing chosen product
            id and amount chosen for this product in json format.
            If amount is bigger that 10 or lower than 1 or
            someone tries to push string in field, returnserror message.
        """
        response = redirect(to=f"/categories/{id}")
        product_in_cart_id = request.POST.get("cart_product")
        product_in_cart_amount = request.POST.get("amount_of_product")
        if not product_in_cart_amount.isnumeric():
            messages.error(
                request, "Błąd dodawania produktu do koszyka, spróbuj ponownie!"
            )
            return response
        elif 1 > int(product_in_cart_amount) > 10:
            messages.error(
                request, "Ilość produktu nie może być większa niż 10 i mniejsza niż 1!"
            )
            return response
        request.session[product_in_cart_id] = product_in_cart_amount
        return response


class ChangeUsernameView(View):
    """View for changing username."""

    def get(self, request, user_id):
        """Method for GET request.

        Args:
            user_id ([int]): Id of user object.

        Returns:
            Form for changing username.
        """
        user = User.objects.get(id=user_id)
        form = ChangeUsernameForm()
        ctx = {"form": form, "logged_user": user}
        return render(request, "change_username.html", ctx)

    def post(self, request, user_id):
        """Method for POST request. Changes username if username is not taken.

        Args:
            user_id ([int]): Id of User objects

        Returns:
            If username is free, saves it and returns user to same site.
        """
        form = ChangeUsernameForm(request.POST)
        user = User.objects.get(id=user_id)
        ctx = {"form": form, "logged_user": user}
        if form.is_valid():
            user.username = form.cleaned_data["username"]
            user.save()
            ctx["info"] = "Pomyślnie zmieniono nazwę użytkownika!"
            return render(request, "change_username.html", ctx)
        return render(request, "change_username.html", ctx)


class UserDetailView(View):
    """View returning users data and form to change that data."""

    def get(self, request, user_id):
        """Method for GET request.

        Args:
            user_id (int): Id of user object accessing site.

        Returns:
            Form with users saved data as initial form data.
        """
        user = User.objects.get(id=user_id)
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        form = ChangeUserData(initial=user_data)
        ctx = {"form": form, "logged_user": user}
        return render(request, "change_user_data.html", ctx)

    def post(self, request, user_id):
        """Method for POST request sent by form

        Args:
            user_id (int): Id of user object accessing site.

        Returns:
            Same site with changed data and information, if proccess was successfull.
            If not, does not change data and returns information that proccess failed.
        """
        form = ChangeUserData(request.POST)
        user = User.objects.get(id=user_id)
        ctx = {"form": form, "logged_user": user}
        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            ctx["info"] = "Pomyślnie zmieniono dane!"
            return render(request, "change_user_data.html", ctx)
        ctx["info"] = "Wystąpił błąd"
        return render(request, "change_user_data.html", ctx)


class CartView(View):

    """View for cart of user"""

    def get_products_from_session(request):
        """Method for getting items from sessions

        Returns:
            List of touples containing Product object and chosen amount by user
        """
        cart_items = []
        for item, amount in request.session.items():
            if item.isnumeric():
                cart_items.append((item, amount))
        return cart_items

    def get_products_cost_from_list(product_list):
        """Method for calculating total cost of products in product_list

        Args:
            product_list (list): list of touples (model product, amount)

        Returns:
            int: returns calculated cost of products in product_list
        """
        total_cost = 0
        for item in product_list:
            total_cost = total_cost + (
                Product.objects.get(pk=item[0]).price * int(item[1])
            )
        return total_cost

    def get(self, request, user_id):
        """

        Args:
            user_id (int/None): id of a user accessing site.
                                If user is not logged in, value can be None.

        Returns:

        """
        product_ids_and_amount = CartView.get_products_from_session(request)
        cost_of_products = CartView.get_products_cost_from_list(product_ids_and_amount)
        cart_products = Product.get_products_and_amounts_from_list(
            product_ids_and_amount
        )
        request.session["cart_products"] = product_ids_and_amount
        request.session["cost"] = float(cost_of_products)
        ctx = {
            "chosen_products": cart_products,
            "cost": cost_of_products,
        }
        return render(request, "cart.html", ctx)

    def post(self, request, user_id):
        """Method for POST request, sent by deletion form.

        Args:
            user_id (int/None): id of a user accessing site.
                                If user is not logged in, value can be None.

        Returns:
            Response redirect to cart view and deletes chosen product from cookies.
        """
        item_to_delete = request.POST.get("delete-btn")
        request.session.pop(item_to_delete)

        return redirect(f"/cart/{user_id}/")


class PaymentFromNewAddressView(View):
    """View for ordering from new address for logged user. If user is not logged,
    its the only avaiable order form."""

    LIST_OF_ORDERD_PRODUCTS = []

    def get(self, request, user_id):
        """Method for GET request. Calculates cost and unloads products form json
        using CartView methods.

        Args:
            user_id (int/None): id of a user accessing site.
                                If user is not logged in, value can be None.

        Returns:
            Form with fields to put order address in, with list of products models,
            amount and total cost.
        """
        cart_products = request.session["cart_products"]
        cost_of_products = request.session["cost"]
        form = UserAddressForm()
        products = Product.get_products_and_amounts_from_list(cart_products)
        PaymentFromNewAddressView.LIST_OF_ORDERD_PRODUCTS = products
        ctx = {
            "form": form,
            "chosen_products": products,
            "cost": cost_of_products,
        }
        return render(request, "new_address_payment.html", ctx)

    def post(self, request, user_id):
        """Method for POST request sent by form. Saves cart model into database,
        with either user id or None, if user was not logged in.

        Args:
            user_id (int/None): id of a user accessing site.
                                If user is not logged in, value can be None.

        Returns:
            Response redirect to main page, with information if process was successfull.
            Delets all product cookies and saves address to user if user was logged in.
        """
        if user_id != "None":
            form = UserAddressForm(request.POST)
            user = User.objects.get(pk=user_id)
            cart = Cart.objects.create(user=user, cost=request.session["cost"])
            if form.is_valid():
                user_address_street = form.cleaned_data["street"]
                user_address_street_num = form.cleaned_data["street_number"]
                user_address_house_num = form.cleaned_data["house_number"]
                user.address_set.get_or_create(
                    street=user_address_street,
                    street_number=user_address_street_num,
                    house_number=user_address_house_num,
                )
        else:
            cart = Cart.objects.create(cost=request.session["cost"])
        for item in PaymentFromNewAddressView.LIST_OF_ORDERD_PRODUCTS:
            CartProduct.objects.create(cart=cart, product=item[0], amount=int(item[1]))
            cart.save()
        cart.clear_session(request)
        response = render(request, "main.html", {"info": "Zamówienie złożone!"})
        return response


class PaymentFromOldAddressView(View):
    """View for ordering from saved address. Accessable only for logged user."""

    LIST_OF_ORDERD_PRODUCTS = []

    def get(self, request, user_id):
        """Same GET method as in Payment From New Address View.
        Only difference is, that form takes list of user addresses when called,
        and user cannot be none"""
        user_addresses = User.objects.get(pk=user_id).address_set.all()
        cart_products = request.session["cart_products"]
        cost_of_products = request.session["cost"]
        form = UserOldAddressForm(address=user_addresses)
        products = Product.get_products_and_amounts_from_list(cart_products)
        PaymentFromNewAddressView.LIST_OF_ORDERD_PRODUCTS = products
        ctx = {
            "chosen_products": products,
            "cost": cost_of_products,
            "form": form,
        }
        return render(request, "old_address_payment.html", ctx)

    def post(self, request, user_id):
        """Method for POST request sent by form. Saves cart object with user id
        and product id with amount is saved in intermediate model, CartProduct

        Args:
            user_id (int): User object id

        Returns:
            Same as POST method in Payment From New Address View, except it does
            not save the address from form.
        """
        user = User.objects.get(pk=user_id)
        cart = Cart.objects.create(user=user, cost=request.session["cost"])
        for item in PaymentFromOldAddressView.LIST_OF_ORDERD_PRODUCTS:
            CartProduct.objects.create(cart=cart, product=item[0], amount=int(item[1]))
        cart.save()
        cart.clear_session(request)
        response = render(request, "main.html", {"info": "Zamówienie złożone!"})

        return response


class CreateNewUserView(View):
    """View for creating new user. Form used is from Django Authentication System"""

    def get(self, request):
        """Method for GET request

        Returns:
            Template with Djangos UserCreationForm
        """
        form = UserCreationForm()
        return render(request, "create_user.html", {"form": form})

    def post(self, request):
        """Method for POST request sent by form. Creates and logs user if
        form is validated correctly

        Returns:
            If form is validated, redirects to main page with user logged.
            If not, returns form with information about error.
        """
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
    """View only for is_staff user. Allows for adding new products to database"""

    def get(self, request):
        """Method for GET request

        Returns:
            Form with fields for creation Product object. Allows for multiple
            relations with Category and Ingredient models
        """

        form = AddProductForm()
        return render(request, "add_product.html", {"form": form})

    def post(self, request):
        """Method for POST request. Creates new product if form is validated.
        Else, returns same page with information that proccess has failed.

        Returns:
            New Product model with relations, if the form is validated.
            Renders same page with information, eithe if the process has been
            successfull or not.
        """
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
    """View for logged user to add new delivery address via form."""

    def get(self, request, user_id):
        """Method for GET request.

        Args:
            user_id (int): Id of User object accessing site

        Returns:
            Form for adding new address
        """
        form = UserAddressForm()
        return render(request, "user_add_new_address.html", {"form": form})

    def post(self, request, user_id):
        """Method for POST request, sent by form. If form is validated,
        creates new Address object and adds relation to logged user.

        Args:
            user_id (int): Id for User object

        Returns:
            Adds new object with relation to logged User. Renders same page with
            information if process was successfull.
        """
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


class UserDeleteAddressView(View):
    """View for deleting saved User addresses"""

    def get(self, request, user_id):
        """Method for GET request.

        Args:
            user_id (int): Id of logged User.

        Returns:
            Form with logged users addresses.
        """
        user_addresses = User.objects.get(pk=user_id).address_set.all()
        form = UserOldAddressForm(address=user_addresses)
        ctx = {"form": form, "user_addresses": user_addresses}
        return render(request, "delete_address.html", ctx)

    def post(self, request, user_id):
        """Method for POST request sent by form.
        Delets selected Address object from database

        Args:
            user_id (int): Id of User object

        Returns:
            If form is validated, deletes Address model and return to same site,
            with information. Else, informs user that address object does not exist.
        """
        user_addresses = User.objects.get(pk=user_id).address_set.all()
        form = UserOldAddressForm(request.POST, address=user_addresses)
        ctx = {
            "form": UserOldAddressForm(address=user_addresses),
            "user_addresses": user_addresses,
        }
        if form.is_valid():
            address = form.cleaned_data["address"]
            address.delete()
            ctx["info"] = "Adres usunięty!"
            return render(request, "delete_address.html", ctx)
        ctx["info"] = "Adres nie istnieje!"
        return render(request, "delete_address.html", ctx)
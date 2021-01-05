"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from Buri_order_site.views import (
    AdminAddProductView,
    CreateNewUserView,
    PaymentView,
    UserAddNewAddress,
    main_page_view,
    category_view,
    CategoryDetailView,
    UserSettingsView,
    CartView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main_page_view, name="buri-main-page"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="buri-main-page")),
    path("categories/", category_view, name="categories"),
    path("categories/<int:id>", CategoryDetailView.as_view(), name="category-details"),
    path(
        "user/<int:user_id>/",
        login_required(UserSettingsView.as_view()),
    ),
    path(
        "user/<int:user_id>/change_password/",
        login_required(
            auth_views.PasswordChangeView.as_view(
                template_name="change_password.html", success_url="/"
            )
        ),
    ),
    path("cart/<user_id>/", CartView.as_view(), name="cart"),
    path("cart/<user_id>/payment/", PaymentView.as_view(), name="payment"),
    path("create_user/", CreateNewUserView.as_view(), name="create_new_user"),
    path(
        "add_product/",
        staff_member_required(AdminAddProductView.as_view(), login_url="/login/"),
        name="admin_add_product",
    ),
    path(
        "user/<int:user_id>/add_new_address/",
        login_required(UserAddNewAddress.as_view()),
        name="add_new_address",
    ),
]

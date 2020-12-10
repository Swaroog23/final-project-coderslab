from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
from Buri_order_site.forms import LogInForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LogginView(View):
    def get(self, request):
        form = LogInForm()
        context = {"form": form}
        return render(request, "login.html", context)

    def post(self, request):
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["login"],
                password=form.cleaned_data["password"],
            )

        return HttpResponse(f"Witaj {user.get_username()}")
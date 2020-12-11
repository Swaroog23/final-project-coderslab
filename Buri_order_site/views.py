from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User


def main_page_view(request):
    return render(request, "main.html")
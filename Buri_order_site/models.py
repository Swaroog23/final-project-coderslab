from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    username = models.CharField(max_length=150)
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)

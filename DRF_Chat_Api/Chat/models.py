from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(max_length=500, null=True)
    location = models.CharField(max_length=30, null=True)
    birth_date = models.DateField(null=True)
    avatar = models.ImageField(
        upload_to="User/avatars/%Y/%m/%d/", null=True)

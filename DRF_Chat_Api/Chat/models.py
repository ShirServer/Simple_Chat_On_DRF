from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings


class User(AbstractUser):
    REQUIRED_FIELDS = ['avatar', ]

    bio = models.TextField(max_length=500, null=True)
    location = models.CharField(max_length=30, null=True)
    birth_date = models.DateField(null=True)
    avatar = models.ImageField(
        upload_to="User/avatars/%Y/%m/%d/", null=True)

    # def save(self, *args, **kwargs):
    #     pass


class Chat(models.Model):
    is_private = models.BooleanField()
    name = models.TextField(max_length=100, null=True)
    avatar = models.ImageField(upload_to="Chat/avatars/%Y/%m/%d/", null=True)
    time_created = models.DateTimeField(auto_now_add=True)


class User_to_Chat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_invitation = models.BooleanField(default=False)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=500)
    answer = models.ForeignKey("Message", on_delete=models.SET_NULL, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=False)


class Message_Files(models.Model):
    message_id = models.ForeignKey("Message", on_delete=models.CASCADE)
    file = models.FileField(upload_to="messages_files/%Y/%m/%d/")

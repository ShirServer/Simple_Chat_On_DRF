from logging import raiseExceptions
from tkinter import N
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from .serializers import *
from .models import *


@api_view(['GET'])
def index(request):
    return Response({"detail": "Это мой RESTfull api для чата на DRF", })


class ChatViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        User_to_Chats_of_user = User_to_Chat.objects.filter(user=request.user)
        for i in User_to_Chats_of_user:
            if i.chat.is_private:

                AnoverUserOfPrivateChat = User_to_Chat.objects.filter(
                    chat=i.chat).exclude(user=request.user)[0].user

                i.chat.avatar = AnoverUserOfPrivateChat.avatar
                i.chat.name = AnoverUserOfPrivateChat.username

        return Response({"chat_list": User_to_ChatDepthSerializer(User_to_Chats_of_user, many=True).data})

    def create(self, request):
        chat = ChatSerializer(data=request.data)
        chat.is_valid(raise_exception=True)
        chat.save()

        if (chat.data["is_private"]):
            with_user = User.objects.filter(
                username=request.data["with_user"])
            if (len(with_user) == 0):  # private
                return Response({"error": "User does not exists"})
            else:
                with_user = with_user[0]

                User_to_Chat_for_user_1 = User_to_ChatSerializer(
                    data={"user": request.user.id, "chat": chat.data['id'], "is_admin": True})
                User_to_Chat_for_user_1.is_valid(raise_exception=True)
                User_to_Chat_for_user_1.save()

                User_to_Chat_for_user_2 = User_to_ChatSerializer(
                    data={"user": with_user.id, "chat": chat.data['id'], "is_admin": True})
                User_to_Chat_for_user_2.is_valid(raise_exception=True)
                User_to_Chat_for_user_2.save()

                return Response({'chat': chat.data,
                                 'User_to_Chat1': User_to_Chat_for_user_1.data,
                                 'User_to_Chat2': User_to_Chat_for_user_2.data})

        else:
            User_to_Chat_for_user_1 = User_to_ChatSerializer(
                data={"user": request.user.id, "chat": chat.data['id'], "is_admin": True})
            User_to_Chat_for_user_1.is_valid(raise_exception=True)
            User_to_Chat_for_user_1.save()

            return Response({'chat': chat.data, 'user_to_chat': User_to_Chat_for_user_1.data})

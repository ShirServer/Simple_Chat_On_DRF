from logging import raiseExceptions
from re import U
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


class ChatPkViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsChatOwner]

    def update(self, request, pk=None):
        instance = get_object_or_404(Chat, pk=pk)

        self.check_object_permissions(self.request, instance)

        serializer = ChatSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"update": serializer.data})

    def destroy(self, request, pk=None):
        chat = get_object_or_404(Chat, pk=pk)

        self.check_object_permissions(self.request, chat)
        chat.delete()

        return Response({"detail": "Chat was suressful delete"})


class ChatRetrivePkViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsChatMember]

    def retrieve(self, request, pk=None):
        instance = Chat.objects.get(pk=pk)

        self.check_object_permissions(self.request, instance)

        return Response({"user list": User_to_ChatDepthUserSerializer(instance.user_to_chat_set.all(), many=True).data})


class InvitationCreateViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsChatOwner]

    def create(self, request, pk=None, user=None):
        user = get_object_or_404(User, pk=user)
        chat = get_object_or_404(Chat, pk=pk)

        self.check_object_permissions(self.request, chat)

        is_admin = request.data.get('is_admin') in ['true', 'True']

        instanse = User_to_Chat.objects.filter(user=user, chat=chat)
        if instanse.exists():
            return Response({"detail": "Юзер уже добавлен"})

        instanse = User_to_Chat(user=user, chat=chat,
                                is_invitation=True, is_admin=is_admin)

        instanse.save()

        return Response({"user_to_chat": User_to_ChatDepthUserSerializer(instanse).data})


class InvitationViewSet(viewsets.ViewSet):
    def update(self, request, pk=None):
        user_to_chat = get_object_or_404(
            Chat, id=pk, user=request.user, is_invitation=True)
        user_to_chat.ia_invitation = False
        user_to_chat.save()
        return Response({"user_to_chat": User_to_ChatDepthUserSerializer(user_to_chat).data})

    def destroy(self, request, pk=None):
        user_to_chat = User_to_Chat.objects.get(id=pk, user=request.user)
        chat = get_object_or_404(Chat, id=pk, user=request.user)
        chat.delete()
        return Response({"detail": "Вы отвергли преглошение в чат"})


class MessageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsChatMember]

    def create(self, request):
        chat = get_object_or_404(Chat, pk=int(request.data.get('chat')))

        self.check_object_permissions(self.request, chat)

        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(chat=chat, author=request.user)

        for i in request.FILES.getlist('files'):
            file = Message_FilesSerializer(
                data={'message_id': serializer.data['id'], 'file': i})
            file.is_valid(raise_exception=True)
            file.save()

        return Response({'message': serializer.data})


class MessagePkViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):
        instance = get_object_or_404(
            Message, id=pk, author=request.user, is_delete=False)

        serializer = MessageSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({'message': serializer.data})

    def destroy(self, request, pk=None):
        instance = get_object_or_404(
            Message, id=pk, author=request.user, is_delete=False)

        instance.is_delete = True
        instance.save()
        return Response({'detail': "message delete is successfully"})

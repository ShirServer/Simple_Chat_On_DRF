from django.urls import path, include, re_path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),

    path('chats',
         ChatViewSet.as_view({'get': 'list', 'post': 'create'}), name='chats'),  # Получени сжатой информации о своих чатах или создать новый чат

    path('chats/<int:pk>/', ChatPkViewSet.as_view(
        {'delete': 'destroy', 'put': 'update'}), name='chatspk'),  # Изменение названия или аватара в чате или его даление

    path('chat/<int:pk>/', ChatRetrivePkViewSet.as_view(
        {'get': 'retrieve', })),  # Получение всей информации об одном чате

    path('chat/messages/<int:pk>/', ChatMessagePkViewSet.as_view({'get': 'retrieve'})),  # Получение всех сообщений в одном чате

    path('invate/<int:pk>/<int:user>', InvitationCreateViewSet.as_view(
        {'post': 'create', })),  # Создание приглашений в чат если в is_admin не true или True, то False

    path('invate/answer/<int:pk>', InvitationViewSet.as_view(
        {'delete': 'destroy', 'put': 'update'})),  # Ответ на приглашение в чат delete-удаляет, put-положительный ответ

    path('message', MessageViewSet.as_view(
         {'post': 'create', })),  # Отправка сообщений

    path('message/<int:pk>', MessagePkViewSet.as_view({'delete': 'destroy', 'put': 'update'}))  # Удаление или редактирование сообщений


]

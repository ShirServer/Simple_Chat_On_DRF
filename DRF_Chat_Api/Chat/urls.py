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
]

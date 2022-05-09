from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),

    path('chats',
         ChatViewSet.as_view({'get': 'list', 'post': 'create'}), name='chats')
]

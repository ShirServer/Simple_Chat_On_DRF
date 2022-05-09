import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import *
from .permissions import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = ("id", "time_created")


class User_to_ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_to_Chat
        fields = '__all__'
        read_only_fields = ("id", )
        # depth = 2

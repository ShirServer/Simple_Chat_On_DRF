import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.conf import settings

from .models import *
from .permissions import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = ("id", "time_created")

    def create(self, validated_data):
        # print(validated_data)
        if validated_data['is_private']:
            return Chat.objects.create(is_private=True)
        else:
            return Chat.objects.create(is_private=False, name=validated_data['name'], avatar=validated_data['avatar'])


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'location', 'birth_date', 'avatar']


class User_to_ChatSerializer(serializers.ModelSerializer):
    # user = PublicUserSerializer()
    class Meta:
        model = User_to_Chat
        fields = '__all__'
        read_only_fields = ("id", )
        # depth = 1


class User_to_ChatDepthSerializer(serializers.ModelSerializer):
    chat = ChatSerializer()

    class Meta:
        model = User_to_Chat
        fields = '__all__'
        read_only_fields = ("id", )


class User_to_ChatDepthUserSerializer(serializers.ModelSerializer):
    chat = ChatSerializer()
    user = PublicUserSerializer()

    class Meta:
        model = User_to_Chat
        fields = '__all__'
        read_only_fields = ("id", )
        # depth = 1

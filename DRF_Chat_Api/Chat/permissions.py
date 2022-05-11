from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAdminUser
from .models import *


class IsChatOwner(BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.user_to_chat_set.get(user=request.user, is_admin=True, is_invitation=False) != None


class IsChatMember(BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.user_to_chat_set.get(user=request.user, is_invitation=False) != None

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view


@api_view(['GET'])
def index(request):
    return Response({"detail": "Это мой RESTfull api для чата на DRF", })

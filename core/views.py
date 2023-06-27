from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from core.filters import UserModelFilter
from core.models import User
from core.serializers import UserViewSetSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = UserModelFilter
    serializer_class = UserViewSetSerializer

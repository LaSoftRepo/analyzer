from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework import viewsets

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

from builtins import print

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    @list_route(methods=['get'], permission_classes=[IsAuthenticated])
    def current_user(self, request, pk=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @detail_route(methods=['patch'], permission_classes=[IsAuthenticated])
    def get_email(self, request, pk=None):
        user = self.get_object()
        is_get_email = request.data.get('is_get_email')
        if is_get_email is not None:
            user.is_get_email = is_get_email
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

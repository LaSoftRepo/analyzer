from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from settings_analyzer.models import Settings, StatusSiteParse, StopWordList
from settings_analyzer.serializers import SettingsSerializer, \
    StatusSerializer, StopWordSerializer, LargeResultsSetPagination


class SettingsViewSet(viewsets.ModelViewSet):
    serializer_class = SettingsSerializer
    queryset = Settings.objects.all()


class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    queryset = StatusSiteParse.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)

    @list_route(methods=['patch'], permission_classes=[IsAuthenticated])
    def save_all(self, request, pk=None):
        for status in request.data:
            instance = StatusSiteParse.objects.get(pk=status.get('id'))
            serializer = StatusSerializer(data=status, instance=instance)
            if serializer.is_valid():
                serializer.save()
        return Response(status=200)


class StopWordViewSet(viewsets.ModelViewSet):
    serializer_class = StopWordSerializer
    pagination_class = LargeResultsSetPagination
    queryset = StopWordList.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering = ('word',)
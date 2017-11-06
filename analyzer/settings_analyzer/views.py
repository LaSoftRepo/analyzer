from django.shortcuts import render
from rest_framework import viewsets

from settings_analyzer.models import Settings
from settings_analyzer.serializers import SettingsSerializer


class SettingsViewSet(viewsets.ModelViewSet):
    serializer_class = SettingsSerializer
    queryset = Settings.objects.all()
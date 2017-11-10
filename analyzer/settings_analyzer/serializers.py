from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.pagination import CustomPagination
from settings_analyzer.models import Settings, StatusSiteParse, StopWordList


class SettingsSerializer(ModelSerializer):

    class Meta:
        model = Settings
        exclude = 'id',


class StatusSerializer(ModelSerializer):

    class Meta:
        model = StatusSiteParse
        fields = ('id', 'name', 'is_enable')


class StopWordSerializer(ModelSerializer):

    class Meta:
        model = StopWordList
        fields = ('id', 'word')


class LargeResultsSetPagination(CustomPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
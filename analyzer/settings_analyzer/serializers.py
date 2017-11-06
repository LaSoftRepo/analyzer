from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from settings_analyzer.models import Settings


class SettingsSerializer(ModelSerializer):
    # settings = serializers.SerializerMethodField()

    class Meta:
        model = Settings
        # fields = '__all__'
        exclude = 'id',

    # def get_settings(self, obj):
    #     return True
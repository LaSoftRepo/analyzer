import json

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from collection.models import Collections


class CollectionsSerializer(ModelSerializer):
    price = serializers.SerializerMethodField()
    phones = serializers.SerializerMethodField()

    class Meta:
        model = Collections
        fields = ('create_at', 'donor', 'id_donor', 'city', 'title',
                  'description', 'link', 'price', 'phones',
                  'name', 'sms_is_send', 'email_is_send')

    @staticmethod
    def get_price(obj):
        return ' '.join((str(obj.price), obj.currency))

    def get_phones(self, obj):
        return json.loads(obj.phones)
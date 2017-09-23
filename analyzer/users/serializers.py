from django.contrib.auth.models import User
from rest_auth.serializers import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name', 'last_name',
                  'password', 'password2')

    def create(self, validated_data):
        if validated_data['password'] == validated_data['password2']:
            del validated_data['password2']
            user = super().create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
        else:
            raise ValidationError({'password': ['Пароли не совпадают']})
        return user
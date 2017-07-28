from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            )

        user.set_password(validated_data['password'])
        user.save()
        user_id_object = { "user_id": user.id }
        return user_id_object

    def signin(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(username=username, password=passwords)

        if user is not None:
            user_id_object = {"user_id": user.id}

            return user_id_object
        else:
            return { "error": "There was an error signing in" }

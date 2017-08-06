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

class PingResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PingResults
        fields = '__all__'

    def save(self, validated_data, user_id, instance_id):
        user = User.objects.get(id=int(user_id))
        print("data going in: ", validated_data)
        ping = PingResults.objects.create(user=user, instance=instance_id,
                                          min_ping=validated_data["min_ping"],
                                          max_ping=validated_data["max_ping"],
                                          avg_ping=validated_data["avg_ping"])

        ping.save()
        ping_object = {"status": "success"}
        return ping_object

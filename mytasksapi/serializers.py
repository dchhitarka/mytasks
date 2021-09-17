from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    # items = serializers.StringRelatedField(many=True)
    class Meta:
        model = Task
        fields = ('id', 'title', 'created_at', 'user')

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        task.save()
        return task


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'title', 'created_at', 'task', 'status')
    def create(self, validated_data):
        item = Item.objects.create(**validated_data)
        item.save()
        return item


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

class RegisterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'username', 'is_active', 'is_admin')
         read_only_fields = ('id', 'is_active', 'is_admin')
    
    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass
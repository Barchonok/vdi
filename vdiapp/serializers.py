from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from .models import *

class HdSerializer(ModelSerializer):

    class Meta:
        model = HardDrive
        fields = '__all__'

class VdiSerializer(ModelSerializer):

    class Meta:
        model = VirtualMachine
        exclude = ('id', 'is_active')

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

class UserDisplaySerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class VdiDisplaySerializer(ModelSerializer):
    hd = HdSerializer()
    user = UserDisplaySerializer()

    class Meta:
        model = VirtualMachine
        fields = '__all__'

class VdiDisplayUserSerializer(ModelSerializer):
    hd = HdSerializer()

    class Meta:
        model = VirtualMachine
        exclude = ('user', )

class VdiConnectSerializer(ModelSerializer):
    class Meta:
        model = VirtualMachine
        fields = ('is_active',)
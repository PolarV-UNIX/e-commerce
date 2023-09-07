from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.utils import timezone
from User.models import *
from datetime import timedelta
import re



""" USER'S AUTH SERIALIZERS """
class UserRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        write_only = True,
        validators = [UniqueValidator(
            queryset = User.objects.all(), 
            message = "this phone number already exists"
        )])
    
    class Meta:
        model = User
        fields = [
            'id',
            'phone', 
            'verification_code',
            ]
    #  VALIDATIONS
    def validate_phone(self, value):
        if len(value) < 11:
            raise serializers.ValidationError(
                "phone number must be 11 digits"
            )
        if not re.match(r"^09\d{9}$", value):
            raise serializers.ValidationError(
                "phone number is invalid phone number must be like this: 09*********"
            )
        return value
    
    # SERAILIZER METHODS
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.generateVerificationCode()
        return user
    
""" USER DEVICE'S IP SERILIZER """
class UserDeviceIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ['ip_address']
    
    

class UserChanePhonenumberSerializer(serializers.ModelSerializer):
    pass


from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.utils import timezone
from User.models import *
from common.utils.common import response
from datetime import timedelta
import re



""" USER'S AUTH SERIALIZERS """
class UserRegisterSerializer(serializers.ModelSerializer):
    
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
        user_device = UserDevice.objects.create(
            user_id = user,
            ip_address = self.context["ip_address"]
        )
        if not user_device:
            raise serializers.ValidationError(
                "create user device has a probelm"
            )
        return user
    
    
""" USER UPDATE DEVICE FIELD """
class UserUpdateDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['device_user']
        
    def update(self, instance, validated_data):
        instance.device_user = validated_data['device_user']
        instance.save()
        return instance
  
    
""" USER DEVICE'S IP SERILIZER """
class UserDeviceIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ['ip_address']
        
    def create(self, validated_data):
        user = User.objects.filter(id=validated_data['id']).first()
        if not user:
            raise serializers.ValidationError(
                "the user_id not found"
            )
        user_device = UserDevice.objects.create(
            ip_address=validated_data['ip_address'],
            user_id=user
        )
        return user_device
    

""" USER CHANGE PHONE NUMBER SERIALIZER"""
class UserChanePhonenumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone']
        
    def update(self, instance, validated_data):
        try:
            instance.phone = validated_data.get('phone', instance.phone)
        except:
            raise serializers.ValidationError(
                "there is a problem with add phone number"
            )
        instance.save()
        return instance


""" USER CHANGE AVATAR SERAIZIER """
class UserChangeAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']
    
    def update(self, instance, validated_data):
        if 'avatar' not in validated_data:
            raise serializers.ValidationError(
                "send the avatar"
            )
        if validated_data['avatar'] is None:
            raise serializers.ValidationError(
                "avatar key has not any value"
            )
        
        instance.avatar = validated_data['avatar']
        instance.save()
        return instance
        
""" USER CHANGE NAME SERAILZIER """
class UserChangeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
    def update(self, instance, validated_data):
        if {'first_name', 'last_name'}.issubset(validated_data):
            instance.first_name = validated_data['first_name']
            instance.last_name = validated_data['last_name']
            instance.save()
            return instance
        else:
            
            if validated_data == {}:
                raise serializers.ValidationError(
                "you don't send any data"
            )
                
            try:
                first_name = validated_data['first_name']
            except:
                try:
                    last_name = validated_data['last_name']
                except:
                    raise serializers.validated_data(
                        "at least must exist one of first name or last name"
                    )
                instance.last_name = last_name
                instance.save()
                return instance
            instance.first_name = first_name
            instance.save()
            return instance
            
        
        
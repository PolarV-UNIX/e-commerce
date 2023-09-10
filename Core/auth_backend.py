from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest



# DEFINE USER OBJECT
CustomUser = get_user_model()

class MyAuthBackend(ModelBackend):
    def authenticate(self, request, phone_number = None, code = None):
        if phone_number is None:    return
        try:
            user = CustomUser.objects.filter(phone_number=phone_number).first()
            return user
            
        except user.DoesNotExist:   return
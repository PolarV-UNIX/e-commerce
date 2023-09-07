from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from common.utils.common import (
    response,
    convertParam,
    getClientIP,
    isTokenExist,
    check_authentication,
)
import json
from User.models import *
from User.serializers.user_serializers import (
    UserRegisterSerializer, 
    UserDeviceIPSerializer
)
from User.jwt import checkToken, genrateJWTToken



""" USER'S APIS """
class UserViewSet(ViewSet):
    # REGISTER
    @action(methods=['post'], detail=False, url_path=r'register', url_name='register')
    def register(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is None:
            try:
                phone = request.data['phone_number']
            except:
                return response(
                    data=None,
                    status=401,
                    message="bad request there is no phone number or token"
                )
            # Store user 
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # Store ip address of device
            serializer_device_ip = UserDeviceIPSerializer(data=getClientIP)
            serializer_device_ip.is_valid(raise_exception=True)
            serializer_device_ip.save()
            
            # Create token for user 
            generate_token = genrateJWTToken(
                user_id=serializer.data['id'],
                phone=serializer.data['phone'],
                code=serializer.data['code']
            )
            
            # Add token to data response
            serializer.data['token'] = generate_token
            return response(
                data=serializer.data,
                status=201,
                message="user create succefuly"
            )
        check_token = checkToken(token)
        if check_token == False:
            return response(
                data=None,
                status=400,
                message="Bad Request try again"
            )   
        return response(
            data=check_token,
            status=200,
            message='User has registerd before and token has expire yet'
        ) 
                     
    # CHANGE PHONE-NUMBER
    @action(methods=['put'], detail=False, url_path=r'changephonenumber', url_name='changephonenumber')
    def changePhoneNumber(self, request):
        pass
    
    # CHANGE AVATAR
    @action(methods=['put'], detail=False, url_path=r'changeavatar', url_name='changeavatar')
    def changeAvatar(self, request):
        pass
    
    # CHANGE NAME
    @action(methods=['put'], detail=False, url_path=r'changename', url_name='changename')
    def changeName(self, request):
        pass
    
    # SETTING EMAIL
    @action(methods=['post'], detail=False, url_path=r'settingemail', url_name='settingemail')
    def settingEmail(self, request):
        pass
    
    # ACCOUNT DELETION
    @action(methods=['delete'], detail=False, url_path=r'deleteaccount', url_name='deleteaccount')
    def deleteAccount(self, request):
        pass
    
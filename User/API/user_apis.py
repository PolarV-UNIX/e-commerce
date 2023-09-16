from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
# CSRF
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from common.utils.common import (
    response,
    convertParam,
    getClientIP,
)
from User.models import *
from User.serializers.user_serializers import (
    UserRegisterSerializer, 
    UserDeviceIPSerializer,
    UserChanePhonenumberSerializer,
    UserChangeAvatarSerializer,
    UserChangeNameSerializer,
    UserUpdateDeviceSerializer
)
from User.jwt import checkToken, genrateJWTToken



""" USER'S APIS """
class UserViewSet(ViewSet):
    """ REGISTER """
    # Disable CSRF protection for this view (for demonstration purposes)
    # in deploy delete the decorator
    @method_decorator(csrf_exempt, name='dispatch')
    @action(methods=['post'], detail=False, url_path=r'register', url_name='register')
    def register(self, request):
        data = request.data
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header pf request"
            )
        if token is None:
            try:
                phone = data['phone']
            except:
                return response(
                    data=None,
                    status=401,
                    message="bad request there is no phone number or token"
                )
            ip = getClientIP(request)
            context = {
                'ip_address': ip
            }
            # Store user
            serializer = UserRegisterSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # somethings 
            user = User.objects.filter(id=serializer.data['id']).first()
            user_device = UserDevice.objects.order_by('-created_at').filter(ip_address=ip).first()
            serializer_device = UserUpdateDeviceSerializer(user, data={
                'device_user': user_device.id
            })
            serializer_device.is_valid(raise_exception=True)
            serializer_device.save()

            # Create token for user 
            generate_token = genrateJWTToken(
                user_id=serializer.data['id'],
                user_phone=serializer.data['phone'],
                code=serializer.data['verification_code']
            )
            
            # Add token to data response
            return response(
                data={
                    "user_data": serializer.data,
                    "token": generate_token
                    },
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
                     
    """ CHANGE PHONE-NUMBER """
    @action(methods=['put'], detail=False, url_path=r'changephonenumber', url_name='changephonenumber')
    def changePhoneNumber(self, request):
        data = request.data
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header pf request"
            )
        try:
            phone = data['phone']
        except:
            return response(
                data=None,
                status=400,
                message="phone number is not exist"
            )
        if not phone.isnumeric():
            return response(
                data=None,
                status=400,
                message="the phone number has non-numeric characters"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem with create token"
            )
        
        user_phone = User.objects.filter(id=check_token['user_id']).first()
        if not user_phone:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
            
        if user_phone.phone == phone:
            return response(
                data=None,
                status=400,
                message="this phone is exist for changing the phone number you need add a new one"
            )
        serializer = UserChanePhonenumberSerializer(user_phone, data=phone)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        fresh_token = check_token
        return response(
            data={
                "main_data":serializer.data,
                "fresh_token": fresh_token
            },
            status=200,
            message="phone changed successfuly"
        )
        
    """ CHANGE AVATAR """
    @action(methods=['put'], detail=False, url_path=r'changeavatar', url_name='changeavatar')
    def changeAvatar(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header pf request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem with create token"
            )
            
        user = User.objects.filter(id=check_token['user_id']).first()
        if not user:
            return response(
                data=None,
                status=401,
                message="user not found"
            )
    
        serializer = UserChangeAvatarSerializer(user ,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response(
            data=serializer.data,
            status=200,
            message="profile photo changed successfuly"
        )
        
    
    """ CHANGE NAME """
    @action(methods=['put'], detail=False, url_path=r'changename', url_name='changename')
    def changeName(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header pf request"
            )
        check_token = checkToken(token)
        user = User.objects.filter(id=check_token['user_id']).first()
        data = request.data
        serializer = UserChangeNameSerializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response(
            data=serializer.data,
            status=200,
            message="firstname/lastname changed successfully"
        )
    
    """  SETTING EMAIL """
    @action(methods=['post'], detail=False, url_path=r'settingemail', url_name='settingemail')
    def settingEmail(self, request):
        pass
    
    """ SETTING GENDER """
    @action(methods=['post'], detail=False, url_path=r'gendercahnge', url_name="gendercahnge")
    def genderChange(self, request):
        pass
    
    """ ACCOUNT DELETION """
    @action(methods=['delete'], detail=False, url_path=r'deleteaccount', url_name='deleteaccount')
    def deleteAccount(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header pf request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem with create token"
            )
        user = User.objects.filter(id=check_token['user_id']).first()
        if user:
            user.delete()
            return response(
                data=None,
                status=200,
                message="user deleted"
            )
        return response(
            data=None,
            status=400,
            message="user not found to delete"
        )
    
from rest_framework.response import Response
import ast, json
from User.models import *
from django.utils import timezone
from django.core.cache import cache
import requests
from Core import settings


""" CUSTOM RESPONSE FUNCTION"""
def response(data = None, status = None, message = None):
    response_data = {
        'data': [data],
        'status': status,
        'message': message
    }
    return Response(data=response_data)

""" CONVERT PARAM OF 'GET' METHOD """
def convertParam(request):
    data = request.GET.dict()
    return data

""" CLIENT IP ADDRESS """
def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

""" CHECK EXIST TOKEN """
def isTokenExist(request):
    if request.META.get('HTTP_AUTHORIZATION') == None:
        return False
    
""" CHECK AUTHENTICATION """
def check_authentication(request):
    isTokenExist(request)
    return getUser(request)

""" DECLARE USER """
def getUser(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is None: return False
    
    try:
        token_cashe = str(request.META.get('HTTP_AUTHORIZATION')).split(" ")[1]
        SECRET_KEY = 'django-insecure-ipc%gmdbmkh63#*3w62oid1rh6_h!!nh%wrj)f4xb+8pv_oq7z'
        import jwt
        decoded_data = jwt.decode(jwt=token_cashe, 
                                  key=SECRET_KEY,
                                  algorithms=["HS256"]
                                  )
        data = cache.get(f"___user_auth_login_email__userToken{decoded_data['user_id']}")
        if data is None:
            # Sending the data to specify url for creating user or find it
            response = requests.post(settings.GET_USER_URL, 
                                     headers={
                                         'Authorization': token
                                     })
            if response.status_code != 200:
                return False
            response = response.json()
            if response['data'] != []:
                if 'id' not in response['data']:
                    return False
                user = User.objects.filter(id=response['data']['id']).first()
                request.User = user
                if user is None:
                    user = User.objects.create(
                        id=response['data']['id'],
                        phone_number=response['data']['phone_number'],
                    )
                request.User = user
                return response['data']
            return response['data']
        return data
    except:
        return False

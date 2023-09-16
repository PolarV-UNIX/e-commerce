from Core.settings import SECRET_KEY
from django.utils import timezone
from django.core.cache import cache
from User.models import User

import datetime
import jwt



def genrateJWTToken(user_id, user_phone, code=None):
    payload = {
        'user_id': user_id,
        'phone': user_phone,
        'exp': timezone.now() + datetime.timedelta(days=60)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # Convert bytes to string for JSON response
    return token

def checkToken(token):
    try:
        token = token.split(" ")[1]
        decoded_data = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=["HS256"]
        )
        user = User.objects.filter(id=decoded_data['user_id']).first()
        if not user:
            return False
        # Diffrene between times by seconds 
        if decoded_data['exp'] > timezone.now().timestamp():
            genrateJWTToken(user.id, user.phone)
        return decoded_data
    except:
        return False
    
def changeJWTTokenPayloadPhoneNumber(payload, phone):
    # Change the phone number in token
    payload['phone'] = phone
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
            
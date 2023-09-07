from Core.settings import SECRET_KEY
from django.utils import timezone
from django.core.cache import cache
from User.models import User

import datetime
import jwt



def genrateJWTToken(user_id, user_phone, code):
    payload = {
        'user_id': user_id,
        'phone': user_phone,
        'code': code,
        'exp': timezone.now() + datetime.timedelta(days=60)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # Convert bytes to string for JSON response
    return token.decode('utf-8')

def checkToken(token, user):
    try:
        token = token.split(" ")[1]
        decoded_data = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=['HS256']
        )
        user = User.objects.filter(id=decoded_data['user_id']).first()
        if decoded_data['exp'] > timezone.now():
            genrateJWTToken(user)
        else:
            return decoded_data
    except:
        return False
            
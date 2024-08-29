import jwt
from datetime import datetime, timedelta, timezone
from postaway_project.settings import SECRET_KEY
from django.shortcuts import redirect


def create_jwt(user):
    payload = {
        'id': user.id,
        'sub': user.username,
        'role': 'user',
        'exp': datetime.now(timezone.utc)+timedelta(minutes=30)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidSignatureError:
        return None
    

def custom_login_required(func):
    def _wrapper_func(request, *args, **kwargs):
        token = request.COOKIES.get('auth_token')
        if token is None or not decode_jwt(token):
            return redirect('signin')
        else:
            return func(request, *args, **kwargs)
    return _wrapper_func
            
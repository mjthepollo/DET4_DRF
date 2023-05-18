
import jwt
from django.http import JsonResponse

from config.settings.base import SECRET_KEY
from user.models import User


def login_required(func):
    def wrapper(*args):
        request = args[0]
        try:
            auth_token = request.headers.get('Authorization', None)
            payload = jwt.decode(auth_token, SECRET_KEY, algorithm='HS256')
            request.user = User.objects.get(id=payload['user_id'])
            return func(*args)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=403)
    return wrapper

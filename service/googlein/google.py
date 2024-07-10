from rest_framework.exceptions import AuthenticationFailed
from .models import AuthUser
from google.oauth2 import id_token
from google.auth.transport import requests
from . import serializers, base_auth
import os


def check_google_auth(google_user: serializers.GoogleAuth) -> dict:
    try:
        id_token.verify_oauth2_token(google_user['token'], requests.Request(), os.getenv('CLIENT_GOOGLE_ID'))
    except ValueError:
        raise AuthenticationFailed(code='403', detail='BadTokenGoogle')
    user, _ = AuthUser.objects.get_or_create(email=google_user['email'])
    return base_auth.create_token(user.id)

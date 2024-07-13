import datetime
from datetime import timedelta
from django.conf import settings
import jwt
from rest_framework.response import Response


def create_token(user_id: int):
    access_token_expires = timedelta(minutes=5)

    return Response({
        'user_id': user_id,
        'access_token': create_access_token(
            data={'user_id': 'user_id'}, expires_delta=access_token_expires
        ),
        'token_type': 'Token',
    })


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.datetime.now() + expires_delta
    else:
        expire = datetime.datetime.now() + timedelta(minutes=15)

    to_encode.update({'exp': expire, 'sub': 'access'})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return Response(encoded_jwt)

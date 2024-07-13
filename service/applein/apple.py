import jwt
import requests
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from social_core.backends.oauth import BaseOAuth2
import os

from social_core.utils import handle_http_errors

with open('AuthKey_WWZ9TCJK3B.p8', 'r', encoding='utf-8') as file:
    clg = file.read()


class AppleOAuth2(BaseOAuth2):
    name = 'apple'
    ACCESS_TOKEN_URL = 'https://appleid.apple.com/auth/token'
    SCOPE_SEPARATOR = ','
    ID_KEY = 'uid'

    @handle_http_errors
    def do_auth(self, access_token, *args, **kwargs):
        response_data = {}
        client_id, client_secret = self.get_key_and_secret()

        headers = {'content-type': "application/x-www-form-urlencoded"}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': access_token,
            'grant_type': 'authorization_code',
        }

        res = requests.post(AppleOAuth2.ACCESS_TOKEN_URL, data=data, headers=headers)
        response_dict = res.json()
        id_token = response_dict.get('id_token', None)

        if id_token:
            decoded = jwt.decode(id_token, '', verify=False)
            response_data.update({'email': decoded['email']}) if 'email' in decoded else None
            response_data.update({'uid': decoded['sub']}) if 'sub' in decoded else None
            response_data.update({'email_verified': decoded['email_verified']}) if 'email_verified' in decoded else None

        response = kwargs.get('response') or {}
        response.update(response_data)
        response.update({'access_token': access_token}) if 'access_token' not in response else None

        kwargs.update({'response': response, 'backend': self})
        return Response(response_data, status=status.HTTP_200_OK)

    def get_user_details(self, response):
        email = response.get('email', None)
        details = {
            'email': email,
        }
        return details

    def get_key_and_secret(self):
        headers = {
            'kid': clg
        }

        payload = {
            'iss': os.getenv('APPLE_ACCOUNT_TEAM_ID'),
            'iat': timezone.now(),
            'exp': timezone.now() + timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': os.getenv('APPLE_ACCOUNT_CLIENT_ID')
        }

        client_secret = jwt.encode(
            payload,
            algorithm='ES256',
            headers=headers,
            key=clg
        )

        return os.getenv('APPLE_ACCOUNT_CLIENT_ID'), client_secret

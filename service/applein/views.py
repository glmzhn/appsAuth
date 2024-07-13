from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AppleAuthSerializer
from .apple import AppleOAuth2
from social_django.strategy import DjangoStrategy
from social_django.models import DjangoStorage


class AppleAuthView(APIView):
    def post(self, request):
        serializer = AppleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        authorization_code = serializer.validated_data['access_token']

        strategy = DjangoStrategy(storage=DjangoStorage)

        backend = AppleOAuth2(strategy=strategy)

        try:
            user_data = backend.do_auth(access_token=authorization_code)
            if user_data:
                email = user_data.get('email')
                uid = user_data.get('uid')

                return Response({
                    'email': email,
                    'uid': uid
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers
from .google import check_google_auth


def google_login(request):
    return render(request, 'googlelogin.html')


@api_view(['POST'])
def google_auth(request):
    google_data = serializers.GoogleAuthSerializer(data=request.data)
    try:
        if google_data.is_valid():
            token = check_google_auth(google_data.data)
            return Response(token)
        else:
            return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

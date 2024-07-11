from rest_framework import serializers


class AppleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()

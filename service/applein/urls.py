from django.urls import path
from .views import AppleAuthView

urlpatterns = [
    path('api/v1/auth/apple/', AppleAuthView.as_view(), name='apple-auth'),
]

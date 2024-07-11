from django.urls import path
from .views import AppleAuthView

urlpatterns = [
    path('auth/apple/', AppleAuthView.as_view(), name='apple-auth'),
]

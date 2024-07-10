from django.urls import path
from . import auth_view

urlpatterns = [
    path('google/', auth_view.google_auth),
    path('login/', auth_view.google_login)
]

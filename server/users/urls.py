from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

urlpatterns = [
    path('token', obtain_auth_token, name='api_token_auth'),
]


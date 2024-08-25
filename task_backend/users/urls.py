from django.urls import path
from . import apis

app_name = 'users'

urlpatterns = [
    path('register/', apis.RegisterApi.as_view(), name='register'),
    path('profile/', apis.ViewProfileApi.as_view(), name='profile'),
    path('profile/verify/', apis.CompleteProfileApi.as_view(), name='profile_verify'),
]

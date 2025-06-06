from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView

app_name = 'users_api'

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login')
]
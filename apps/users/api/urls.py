from django.urls import path
from .views import UserRegistrationAPIView

app_name = 'users_api'

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
]
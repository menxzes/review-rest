from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .domain.models import User

class CustomUserCreationForm(UserChangeForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'nome')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('email', 'nome', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
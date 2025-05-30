from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUseAdmin
from .domain.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserAdmin(BaseUseAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'nome', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'nome',)
    ordering = ('email',)

    # fieldsets para ajustar formulário devido a remoção de `username`
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'first_name', 'last_name')}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome'),
        }),
    )

admin.site.register(User, UserAdmin)
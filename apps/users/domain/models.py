from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.users.domain.managers import CustomUserManager

class User(AbstractUser):
    # remoção do username para usar o email como fator de login
    username = None

    # campos
    nome = models.CharField(_("Nome completo"), max_length=255)
    email = models.EmailField(_("Endereço de email"), unique=True)

    # define 'email' como campo de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

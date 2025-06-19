from django.db import models
# Importe seu modelo User customizado
from apps.users.domain.models import User
from django.utils.translation import gettext_lazy as _

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    # Adicione outros campos necessários

    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    # --- CORREÇÃO AQUI ---
    # Remova user_name e adicione uma ForeignKey para User
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews') # Nome de campo 'user'
    # --- FIM DA CORREÇÃO ---
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Altere para usar o email ou nome do usuário relacionado
        return f"Review de {self.user.email} para {self.restaurant.nome}" # Ou self.user.nome se User tiver campo 'nome'
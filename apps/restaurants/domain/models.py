from django.db import models
from django.utils.translation import gettext_lazy as _

class Restaurant(models.Model):
    nome = models.CharField(_("Nome do Restaurante"), max_length=200)
    endereco = models.CharField(_("Endereço"), max_length=255)
    tipo_culinaria = models.CharField(_("Tipo de Culinária"), max_length=100)
    telefone = models.CharField(_("Telefone"), max_length=20, blank=True, null=True) # telefone opcional
    descricao = models.TextField(_("Descrição"), blank=True, null=True) # descrição opcional

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = _("Restaurante")
        verbose_name_plural = _("Restaurantes")
        ordering = ['nome'] # Ordena por nome

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Review(models.Model):
    restaurante = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name=_("Restaurante")
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name=_("Usuário")
    )
    nota = models.IntegerField(
        _("Nota"),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(_("Comentário"))
    data_avaliacao = models.DateTimeField(_("Data da Avaliação"), auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.usuario.email} para {self.restaurante.nome} - Nota: {self.nota}"
    
    class Meta:
        verbose_name = _("Avaliação")
        verbose_name_plural = _("Avaliações")
        ordering = ['-data_avaliacao'] # mais recentes primeiro e usuario comenta apenas uma vez
        unique_together = ('restaurante', 'usuario')

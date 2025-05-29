from django.contrib import admin
from .domain.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurante', 'usuario', 'nota', 'data_avaliacao')
    search_fields = ('restaurante__nome', 'usuario__email', 'comentario')
    list_filter = ('nota', 'data_avaliacao', 'restaurante')
    ordering = ('-data_avaliacao',)
    readonly_fields = ('data_avaliacao',)

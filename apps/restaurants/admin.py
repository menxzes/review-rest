from django.contrib import admin
from .domain.models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_culinaria', 'endereco', 'telefone')
    search_fields = ('nome', 'tipo_culinaria', 'endereco')
    list_filter = ('tipo_culinaria',)
    ordering = ('nome',)

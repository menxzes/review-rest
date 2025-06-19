from django.contrib import admin
from .domain.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # --- CORREÇÃO AQUI ---
    # Altere 'user_name' para 'user'
    list_display = ('restaurant', 'user', 'rating', 'date') 
    # --- FIM DA CORREÇÃO ---
    ordering = ('-date',) 
    readonly_fields = ('date',) 
    list_filter = ('rating', 'date', 'restaurant') 
    # Adapte search_fields se user_name era usado para busca e agora o user é ForeignKey
    search_fields = ('comment', 'user__email', 'user__nome') # Exemplo para buscar no user relacionado

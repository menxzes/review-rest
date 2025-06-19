# apps/restaurants/api/urls.py

from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet

# Não precisamos de 'app_name' ou 'urlpatterns' aqui diretamente se só vamos exportar o router.

router = DefaultRouter()
router.register(r'', RestaurantViewSet, basename='restaurant') # <-- Mude 'restaurants' para '' (string vazia)
# Isso significa que o RestaurantViewSet será o "root" deste arquivo de URLs.
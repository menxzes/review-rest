# apps/reviews/api/urls.py

from rest_framework.routers import DefaultRouter
from apps.reviews.api.views import ReviewViewSet # Importa apenas o ViewSet

# Crie uma instância do DefaultRouter
router = DefaultRouter()

# Registre o ReviewViewSet com o router
# O basename 'reviews' é usado para gerar os nomes das URLs (e.g., 'reviews-list', 'reviews-detail')
router.register(r'reviews', ReviewViewSet, basename='reviews')

# As URLs geradas pelo router serão automaticamente incluídas aqui
urlpatterns = router.urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet

app_name = 'restaurants_api'

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('', include(router.urls)),
]
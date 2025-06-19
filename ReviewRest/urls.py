"""
URL configuration for ReviewRest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter # Importa DefaultRouter
from apps.reviews.api.views import ReviewViewSet # Importa ReviewViewSet
from apps.restaurants.api.views import RestaurantViewSet # Importa RestaurantViewSet
from apps.users.api import urls as users_urls # Importa o módulo urls de users

# Crie os routers aqui para cada app, se preferir centralizá-los
router_reviews = DefaultRouter()
router_reviews.register(r'reviews', ReviewViewSet, basename='review') # Basename 'review' para reviews

router_restaurants = DefaultRouter()
router_restaurants.register(r'restaurants', RestaurantViewSet, basename='restaurant') # Basename 'restaurant' para restaurants

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inclui as URLs geradas pelo router de reviews
    path('api/', include(router_reviews.urls)), # review URLs: /api/reviews/, /api/reviews/{id}/
    
    # Inclui as URLs geradas pelo router de restaurants
    path('api/', include(router_restaurants.urls)), # restaurant URLs: /api/restaurants/, /api/restaurants/{id}/
    
    # Inclui as URLs do app users (se users/api/urls.py já usa path/router ou api_view)
    path('api/users/', include(users_urls)),
]

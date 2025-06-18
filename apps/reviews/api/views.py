# apps/reviews/views.py
from rest_framework import generics
from models import Review, Restaurant
from .serializers import RestaurantSerializer, ReviewSerializer

class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurante')
        if restaurant_id:
            return Review.objects.filter(restaurant_id=restaurant_id)
        return Review.objects.all()

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer  # Crie este serializer

class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
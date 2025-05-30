from rest_framework import serializers
from apps.restaurants.domain.models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    # serializer para o modelo Restaurant
    class Meta:
        model = Restaurant

        fields = '__all__'
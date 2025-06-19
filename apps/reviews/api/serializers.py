from rest_framework import serializers
from apps.reviews.domain.models import Review
from apps.users.api.serializers import UserSerializer
from apps.restaurants.domain.models import Restaurant
from apps.reviews.application.exceptions import UserAlreadyReviewedError

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Review
        # *** ESTA É A LINHA CRÍTICA ***
        # O campo 'restaurant' DEVE estar incluído na tupla 'fields'.
        fields = ['id', 'restaurant', 'usuario', 'rating', 'comment', 'date'] 
        read_only_fields = ['id', 'usuario', 'date']
    
    def validate(self, data):
        """
        Validação para garantir que o usuário não avalie o mesmo restaurante mais de uma vez.
        """
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or not request.user.is_authenticated:
            raise serializers.ValidationError("É necessário estar autenticado para fazer uma avaliação.")
        
        user = request.user
        restaurant_instance = data.get('restaurant')
        
        # --- ADIÇÃO PARA DEBUG ---
        print(f"DEBUG: ReviewSerializer.validate - type(restaurant_instance): {type(restaurant_instance)}, value: {restaurant_instance}")


        if data.get('rating') is None:
            raise serializers.ValidationError({"rating": "A nota é obrigatória."})
        if not data.get('comment', '').strip():
            raise serializers.ValidationError({"comment": "O comentário não pode estar vazio."})

        if Review.objects.filter(restaurant_id=restaurant_instance.id, user=user).exists():
            if self.instance is None or (self.instance and self.instance.restaurant != restaurant_instance):
                raise serializers.ValidationError({"non_field_errors": ["Você já avaliou este restaurante."]})
        return data


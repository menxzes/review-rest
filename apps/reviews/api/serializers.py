from rest_framework import serializers
from apps.reviews.domain.models import Review
from apps.users.api.serializers import UserSerializer
from apps.restaurants.domain.models import Restaurant

class ReviewSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    restaurante = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'restaurante', 'usuario', 'nota', 'comentario', 'data_avaliacao']
        read_only_fields = ['id', 'usuario', 'data_avaliacao']
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def validate(self, data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or not request.user.is_authenticated:
            raise serializers.ValidationError("É necessário estar autenticado para fazer uma avaliação.")
        
        user = request.user
        restaurante_instance = data.get('restaurante')

        if restaurante_instance:
            if Review.objects.filter(restaurante=restaurante_instance, usuario=user).exists:
                if not self.instance:
                    raise serializers.ValidationError("Você já avaliou este restaurante.")
        return data

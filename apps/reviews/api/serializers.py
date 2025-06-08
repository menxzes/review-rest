from rest_framework import serializers
from apps.reviews.domain.models import Review
from apps.users.api.serializers import UserSerializer
from apps.restaurants.domain.models import Restaurant
from apps.reviews.application.exceptions import UserAlreadyReviewedError

class ReviewSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    restaurante = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'restaurante', 'usuario', 'nota', 'comentario', 'data_avaliacao']
        read_only_fields = ['id', 'usuario', 'data_avaliacao']
    
    def validate(self, data):
        """
        Validação para garantir que o usuário não avalie o mesmo restaurante mais de uma vez.
        Esta validação age como uma "pré-validação" para feedback rápido na API.
        A validação final e a exceção de negócio são tratadas no serviço.
        """
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or not request.user.is_authenticated:
            raise serializers.ValidationError("É necessário estar autenticado para fazer uma avaliação.")
        
        user = request.user
        restaurante_instance = data.get('restaurante')

        if restaurante_instance:
            # Verifica se já existe uma avaliação do USUÁRIO para o RESTAURANTE
            # para casos de criação (self.instance é None para criações)
            # ou se a instância sendo validada NÃO é a mesma que já existe (para atualizações)
            if Review.objects.filter(restaurante=restaurante_instance, usuario=user).exists():
                # Se estamos criando e já existe uma avaliação, ou
                # se estamos atualizando e a avaliação existente não é a que estamos editando
                # (isso evita o erro de "unique_together" ao salvar a mesma review)
                if self.instance is None or (self.instance and self.instance.restaurante != restaurante_instance):
                    # Podemos levantar a mesma exceção que o serviço levantaria,
                    # ou uma ValidationError genérica que o serializer irá capturar.
                    # Usar a exceção do serviço pode ajudar na consistência das mensagens.
                    raise serializers.ValidationError({"non_field_errors": ["Você já avaliou este restaurante."]})
                    # Ou, se quisermos usar a exceção customizada diretamente (requer tratamento no serializer):
                    # raise UserAlreadyReviewedError("Você já avaliou este restaurante.")
        return data

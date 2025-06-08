from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from apps.reviews.domain.models import Review
from apps.reviews.api.serializers import ReviewSerializer
from apps.reviews.api.permissions import IsOwnerOrAdmin
from apps.reviews.infrastructure.repositories import ReviewRepository
from apps.reviews.application.services import (
    ReviewCreationService,
    ReviewUpdateService,
    ReviewDeletionService,
    ReviewQueryService
)
from apps.reviews.application.exceptions import (
    ReviewNotFoundError,
    UserAlreadyReviewedError,
    UnauthorizedReviewActionError
)
from apps.restaurants.domain.models import Restaurant
from apps.users.domain.models import User

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-data_avaliacao')
    serializer_class = ReviewSerializer

    review_repository = ReviewRepository()
    review_creation_service = ReviewCreationService(review_repository)
    review_update_service = ReviewUpdateService(review_repository)
    review_deletion_service = ReviewDeletionService(review_repository)
    review_query_service = ReviewQueryService(review_repository)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        else: # 'list', 'retrieve'
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = self.queryset
        restaurante_id = self.request.query_params.get('restaurante')
        if restaurante_id:
            try:
                restaurant = Restaurant.objects.get(id=restaurante_id)
                queryset = self.review_query_service.get_reviews_for_restaurant(restaurant)
            except Restaurant.DoesNotExist:
                queryset = Review.objects.none()
        return queryset
    
    def perform_create(self, serializer):
        
        request_user: User = self.request.user
        restaurante_id = serializer.validated_data['restaurante'].id # Pega o ID da instância do restaurante
        nota = serializer.validated_data['nota']
        comentario = serializer.validated_data['comentario']

        try:
            # instância completa do restaurante para o serviço
            restaurante_instance = Restaurant.objects.get(id=restaurante_id)
            
            review = self.review_creation_service.create_review(
                restaurante=restaurante_instance,
                usuario=request_user,
                nota=nota,
                comentario=comentario
            )
            serializer.instance = review # Atribui a instância criada para o serializer
        except UserAlreadyReviewedError as e:
            raise serializers.ValidationError({"non_field_errors": [str(e)]}, code='unique_review')
        except Restaurant.DoesNotExist:
            raise serializers.ValidationError({"restaurante": ["Restaurante não encontrado."]}, code='invalid_restaurant')
        except Exception as e:
            # Logar o erro completo aqui
            raise serializers.ValidationError({"detail": f"Erro inesperado ao criar avaliação: {e}"})

    def perform_update(self, serializer):
    
        review_id = self.kwargs.get(self.lookup_field)
        request_user: User = self.request.user 

        nota = serializer.validated_data.get('nota', serializer.instance.nota) # Use valor atual se não for fornecido
        comentario = serializer.validated_data.get('comentario', serializer.instance.comentario) # Use valor atual se não for fornecido

        try:
            updated_review = self.review_update_service.update_review(
                review_id=review_id,
                nota=nota,
                comentario=comentario,
                requesting_user=request_user
            )
            serializer.instance = updated_review # Atribui a instância atualizada para o serializer
        except ReviewNotFoundError:
            raise Http404("Avaliação não encontrada.") # Ou um erro 400 se preferir mais específico
        except UnauthorizedReviewActionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Logar o erro completo aqui
            return Response({"detail": f"Erro inesperado ao atualizar avaliação: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_destroy(self, instance: Review):
        """
        Deleta uma avaliação existente usando o serviço de deleção.
        """
        review_id = instance.id # Obtém o ID da instância que seria deletada
        request_user: User = self.request.user # Garante que o tipo é User

        try:
            self.review_deletion_service.delete_review(
                review_id=review_id,
                requesting_user=request_user
            )
        except ReviewNotFoundError:
            raise Http404("Avaliação não encontrada.")
        except UnauthorizedReviewActionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Logar o erro completo aqui
            return Response({"detail": f"Erro inesperado ao deletar avaliação: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

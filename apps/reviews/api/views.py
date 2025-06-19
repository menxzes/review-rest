from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework import serializers # Para serializers.ValidationError
from django.http import Http404

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
    queryset = Review.objects.all().order_by('-date') # Confirme que é '-date'
    serializer_class = ReviewSerializer

    review_repository = ReviewRepository()
    review_creation_service = ReviewCreationService(review_repository)
    review_update_service = ReviewUpdateService(review_repository)
    review_deletion_service = ReviewDeletionService(review_repository)
    review_query_service = ReviewQueryService(review_repository)

    def get_permissions(self):
        """
        Define as permissões para cada ação.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        else: # 'list', 'retrieve'
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    review_query_service = ReviewQueryService(review_repository)

    def get_queryset(self):
        queryset = self.queryset
        restaurant_id = self.request.query_params.get('restaurant') 
        if restaurant_id:
            try:
                restaurant = Restaurant.objects.get(id=restaurant_id)
                queryset = self.review_query_service.get_reviews_for_restaurant(restaurant)
            except Restaurant.DoesNotExist:
                queryset = Review.objects.none()
        return queryset


    def perform_create(self, serializer):
        """
        Cria uma nova avaliação usando o serviço de criação.
        """
        request_user: User = self.request.user
        restaurant_id = serializer.validated_data['restaurant'].id # OK, aqui é o ID do restaurante
        
        rating = serializer.validated_data['rating']
        comment = serializer.validated_data['comment']

        try:
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            
            # --- CORREÇÃO AQUI ---
            # O parâmetro do serviço agora é 'restaurant'
            review = self.review_creation_service.create_review(
                restaurant=restaurant_instance, # Corrigido: passando para 'restaurant'
                user=request_user,
                rating=rating,
                comment=comment
            )
            # --- FIM DA CORREÇÃO ---
            serializer.instance = review
        except UserAlreadyReviewedError as e:
            raise serializers.ValidationError({"non_field_errors": [str(e)]}, code='unique_review')
        except Restaurant.DoesNotExist:
            raise serializers.ValidationError({"restaurant": ["Restaurante não encontrado."]}, code='invalid_restaurant')
        except Exception as e:
            raise serializers.ValidationError({"detail": f"Erro inesperado ao criar avaliação: {e}"})


    def perform_update(self, serializer):
        """
        Atualiza uma avaliação existente usando o serviço de atualização.
        """
        review_id = self.kwargs.get(self.lookup_field)
        request_user: User = self.request.user

        rating = serializer.validated_data.get('rating', serializer.instance.rating)
        comment = serializer.validated_data.get('comment', serializer.instance.comment)

        try:
            updated_review = self.review_update_service.update_review(
                review_id=review_id,
                rating=rating,
                comment=comment,
                requesting_user=request_user
            )
            serializer.instance = updated_review
        except ReviewNotFoundError:
            raise Http404("Avaliação não encontrada.")
        except UnauthorizedReviewActionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
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
        pass
from typing import List, Optional
from apps.reviews.domain.models import Review
from apps.reviews.infrastructure.repositories import ReviewRepository
from apps.users.domain.models import User
from apps.restaurants.domain.models import Restaurant
from apps.reviews.application.exceptions import ReviewNotFoundError, UserAlreadyReviewedError, UnauthorizedReviewActionError

class ReviewCreationService:

    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository
    
    def create_review(self, restaurante: Restaurant, usuario: User, nota: int, comentario: str) -> Review:
        # Verificação da regra de negócio: um usuário só pode avaliar um restaurante uma vez.
        existing_review = self.review_repository.get_user_review_for_restaurant(usuario, restaurante)
        if existing_review:
            raise UserAlreadyReviewedError(f"O usuário {usuario.email} já avaliou o restaurante {restaurante.nome}.")
        
        return self.review_repository.create(restaurante, usuario, nota, comentario)

class ReviewUpdateService:
    
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository
    
    def update_review(self, review_id: int, nota: int, comentario: str, requesting_user: User) -> Review:
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundError(f"Avaliação com ID {review_id} não encontrada.")
        
        if review.usuario != requesting_user and not requesting_user.is_staff:
            raise UnauthorizedReviewActionError("Você não tem permissão para atualizar esta avaliação.")
        
        return self.review_repository.update(review, nota, comentario)

class ReviewDeletionService:
    
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository
    
    def delete_review(self, review_id: int, requesting_user: User):
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundError(f"Avaliação com ID {review_id} não encontrada.")
        
        if review.usuario != requesting_user and not requesting_user.is_staff:
            raise UnauthorizedReviewActionError("Você não tem permissão para deletar esta avaliação.")
            
        self.review_repository.delete(review)

class ReviewQueryService:
    
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        
        return self.review_repository.get_by_id(review_id)

    def get_reviews_for_restaurant(self, restaurant: Restaurant) -> List[Review]:
        
        return self.review_repository.get_reviews_by_restaurant(restaurant)

    def get_user_review_for_restaurant(self, user: User, restaurant: Restaurant) -> Optional[Review]:
        
        return self.review_repository.get_user_review_for_restaurant(user, restaurant)

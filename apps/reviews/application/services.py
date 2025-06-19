from typing import List, Optional
from apps.reviews.domain.models import Review
from apps.reviews.infrastructure.repositories import ReviewRepository
from apps.users.domain.models import User
from apps.restaurants.domain.models import Restaurant
from apps.reviews.application.exceptions import ReviewNotFoundError, UserAlreadyReviewedError, UnauthorizedReviewActionError

class ReviewCreationService:
    """
    Serviço para criar novas avaliações.
    """
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def create_review(self, restaurant: Restaurant, user: User, rating: int, comment: str) -> Review:
        existing_review = self.review_repository.get_user_review_for_restaurant(user, restaurant)
        if existing_review:
            raise UserAlreadyReviewedError(f"O usuário {user.email} já avaliou o restaurante {restaurant.nome}.")
        
        return self.review_repository.create(restaurant, user, rating, comment)


class ReviewUpdateService:
    """
    Serviço para atualizar avaliações existentes.
    """
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository


    def update_review(self, review_id: int, rating: int, comment: str, requesting_user: User) -> Review:

        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundError(f"Avaliação com ID {review_id} não encontrada.")
        

        if review.user != requesting_user and not requesting_user.is_staff:
            raise UnauthorizedReviewActionError("Você não tem permissão para atualizar esta avaliação.")
            
        return self.review_repository.update(review, rating, comment)

class ReviewDeletionService:
    
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository
    
    def delete_review(self, review_id: int, requesting_user: User):
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundError(f"Avaliação com ID {review_id} não encontrada.")
        
        if review.user != requesting_user and not requesting_user.is_staff:
            raise UnauthorizedReviewActionError("Você não tem permissão para deletar esta avaliação.")
            
        self.review_repository.delete(review)
    pass

class ReviewQueryService:
    
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        
        return self.review_repository.get_by_id(review_id)

    def get_reviews_for_restaurant(self, restaurant: Restaurant) -> List[Review]:
        return self.review_repository.get_reviews_by_restaurant(restaurant)


    def get_user_review_for_restaurant(self, user: User, restaurant: Restaurant) -> Optional[Review]:
        return self.review_repository.get_user_review_for_restaurant(user, restaurant)

from typing import Optional, List
from apps.reviews.domain.models import Review
from apps.users.domain.models import User
from apps.restaurants.domain.models import Restaurant

class ReviewRepository:

    def create(self, restaurante: Restaurant, usuario: User, nota: int, comentario: str) -> Review:
        review = Review.objects.create(
            restaurante=restaurante,
            usuario=usuario,
            nota=nota,
            comentario=comentario,
        )
        return review
    
    def get_by_id(self, review_id: int) -> Optional[Review]:
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None
    
    def get_review_by_restaurant(self, restaurant: Restaurant) -> List[Review]:
        return list(Review.objects.filter(restaurante=restaurant).order_by('-data_avaliacao'))
    
    def get_user_review_for_restaurant(self, user: User, restaurant: Restaurant) -> Optional[Review]:
        try:
            return Review.objects.get(usuario=user, restaurante=restaurant)
        except Review.DoesNotExist:
            return None
        
    def update(self, review: Review, nota: int, comentario: str) -> Review:
        review.nota = nota
        review.comentario = comentario
        review.save()
        return review

    def delete(self, review: Review):
        review.delete()

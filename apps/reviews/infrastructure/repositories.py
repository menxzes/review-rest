from typing import Optional, List
from apps.reviews.domain.models import Review
from apps.users.domain.models import User
from apps.restaurants.domain.models import Restaurant

class ReviewRepository:

    def create(self, restaurant: Restaurant, user: User, rating: int, comment: str) -> Review:
        review = Review.objects.create(
            restaurant=restaurant, # Corrigido: usando o nome de campo real
            user=user,
            rating=rating,
            comment=comment
        )
        return review
    
    def get_by_id(self, review_id: int) -> Optional[Review]:
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None
        
        pass
    
    def get_reviews_by_restaurant(self, restaurant: Restaurant) -> List[Review]:
        return list(Review.objects.filter(restaurant_id=restaurant.id).order_by('-date'))
    
    def get_user_review_for_restaurant(self, user: User, restaurant: Restaurant) -> Optional[Review]:
        return Review.objects.filter(user=user, restaurant=restaurant).first()
        
    def update(self, review: Review, rating: int, comment: str) -> Review:
        review.rating = rating # Corrigido
        review.comment = comment # Corrigido
        review.save()
        return review

    def delete(self, review: Review):
        review.delete()
        pass

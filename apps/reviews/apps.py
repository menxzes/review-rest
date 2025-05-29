from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reviews'

    def ready(self):
        try:
            import apps.reviews.domain.models
        except ImportError:
            pass

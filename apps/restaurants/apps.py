from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.restaurants'

    def ready(self):
        try:
            import apps.restaurants.domain.models
        except ImportError:
            pass

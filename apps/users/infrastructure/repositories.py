from apps.users.domain.models import User

class UserRepository:
    def create_user(self, email, nome, password, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = User.objects.create_user(
            email=email,
            nome=nome,
            password=password,
            **extra_fields,
        )
        return user
    
    def get_by_email(self, email: str):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
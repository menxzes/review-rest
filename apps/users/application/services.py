from apps.users.domain.models import User
from apps.users.infrastructure.repositories import UserRepository
from .exceptions import UserAlreadyExistsError

class UserRegistrationService:
    def __init__(self, user_repository: UserRepository):
        
        self.user_repository = user_repository
    
    def register_user(self, email: str, nome: str, password: str, first_name: str = '', last_name: str = '') -> User:
        # verificar se user já existe
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise UserAlreadyExistsError(f"Um usuário com o email {email} já existe.")
        
        # se não existir, cria-o
        extra_fields = {
            'first_name': first_name,
            'last_name': last_name,
        }

        new_user = self.user_repository.create_user(
            email=email,
            nome=nome,
            password=password,
            **extra_fields,
        )
        return new_user

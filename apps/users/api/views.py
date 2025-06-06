from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserSerializer # UserLoginSerializer também, se estiver no mesmo arquivo
# Importe o serviço e o repositório, e a exceção customizada
from apps.users.application.services import UserRegistrationService
from apps.users.application.exceptions import UserAlreadyExistsError
from apps.users.infrastructure.repositories import UserRepository

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            # Os dados foram validados pelo serializer.
            # Agora, usamos o serviço para registrar o usuário.
            
            # 1. Crie instâncias do repositório e do serviço
            # Em um projeto maior, você poderia usar injeção de dependência aqui.
            user_repo = UserRepository()
            registration_service = UserRegistrationService(user_repository=user_repo)
            
            # Pega os dados validados necessários para o serviço
            validated_data = serializer.validated_data
            email = validated_data.get('email')
            nome = validated_data.get('nome')
            password = validated_data.get('password')
            first_name = validated_data.get('first_name', '') # Fornece valor padrão
            last_name = validated_data.get('last_name', '')  # Fornece valor padrão

            try:
                # 2. Chame o método do serviço para registrar o usuário
                user = registration_service.register_user(
                    email=email,
                    nome=nome,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # 3. Se bem-sucedido, serialize o usuário criado para a resposta
                response_data_serializer = UserSerializer(user)
                return Response(response_data_serializer.data, status=status.HTTP_201_CREATED)
            
            except UserAlreadyExistsError as e:
                # 4. Se o serviço levantar UserAlreadyExistsError, retorne um erro 400
                # (ou 409 Conflict, que também é apropriado para este caso)
                return Response({"email": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Para outros erros inesperados do serviço
                # Idealmente, registre este erro (logging)
                return Response({"detail": "Ocorreu um erro durante o registro."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Se os dados do serializer não forem válidos, retorna os erros de validação do serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data, 
                                         context={'request': request})
        
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data_serializer = UserSerializer(user)
        
        return Response({
            'token': token.key,
            'user': user_data_serializer.data
        }, status=status.HTTP_200_OK)

from rest_framework import serializers
from apps.users.domain.models import User
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    # serializers para exibir informações do usuário
    class Meta:
        model = User
        fields = ['id', 'email', 'nome', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']

class UserRegistrationSerializer(serializers.ModelSerializer):
    # campo email explicito para UniqueValidator
    email = serializers.EmailField(
        required = True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Este endereço de email já está registrado.")]
    )
    
    # serializers para registro
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirme a senha")

    class Meta:
        model = User
        fields = ['email', 'nome', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        attrs.pop('password2')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            nome = validated_data['nome'],
            password = validated_data['password'],
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', '')
        )
        return user
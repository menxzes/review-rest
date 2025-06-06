from rest_framework import serializers
from apps.users.domain.models import User
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    # serializers para exibir informações do usuário
    class Meta:
        model = User
        fields = ['id', 'email', 'nome', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        # Mantemos o UniqueValidator para feedback rápido na API
        validators=[UniqueValidator(queryset=User.objects.all(), message="Este endereço de email já está registrado.")]
    )
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirme a senha")
    # O campo 'nome' é herdado do modelo e é obrigatório por padrão.

    class Meta:
        model = User
        # 'nome' é um campo do modelo User e será incluído.
        fields = ['email', 'nome', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            # 'nome' é obrigatório por padrão pois no modelo User não tem blank=True nem null=True
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "As senhas não coincidem."}) # Mudei o erro para password2
        # Não precisamos mais remover 'password2' aqui, pois não vamos chamar um método 'create'
        # que espera apenas campos do modelo. A view pegará os campos necessários de validated_data.
        return attrs

class UserLoginSerializer(serializers.Serializer):
    # serializers para validação de dados do user
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Senha"),
        style={'input_type': 'password'},
        trim_whitespace=False # Não remove espaços em branco da senha
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            # Se a autenticação falhar, authenticate() retorna None
            if not user:
                msg = _('Não foi possível fazer login com as credenciais fornecidas.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('É necessário incluir "email" e "senha".')
            raise serializers.ValidationError(msg, code='authorization')

        # Se a autenticação for bem-sucedida, o usuário é retornado nos atributos validados.
        attrs['user'] = user
        return attrs
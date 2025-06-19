# review-rest
Um sistema para gerenciar e avaliar restaurantes, permitindo que usuários se registrem, visualizem restaurantes e enviem avaliações, enquanto administradores podem gerenciar os dados dos restaurantes.

## Casos de Uso

### 1. Registro e Autenticação de Usuário
Usuários podem criar contas e fazer login para acessar funcionalidades autenticadas, como o envio de avaliações.

### 2. Navegação de Restaurantes
Qualquer usuário pode visualizar uma lista de restaurantes e detalhes específicos sobre cada um.

### 3. Envio e Gerenciamento de Avaliações
Usuários autenticados podem submeter, editar e excluir suas próprias avaliações. Administradores têm controle total sobre todas as avaliações.

### 4. Gerenciamento de Restaurantes pelo Administrador
Administradores podem adicionar, editar e excluir informações de restaurantes no sistema.

## Estrutura do Projeto

O projeto é dividido em um back-end (Django com Django REST Framework) e um front-end (HTML, CSS, JavaScript puro).

### Back-end (Django REST Framework)
Localizado no diretório principal e nos subdiretórios `apps/`.
- `apps/users/`: Gerencia o registro, login e perfis de usuário.
- `apps/restaurants/`: Lida com a criação, leitura, atualização e exclusão de dados de restaurantes.
- `apps/reviews/`: Responsável pelo gerenciamento das avaliações de restaurantes.
- `ReviewRest/settings.py`: Configurações gerais do Django.
- `ReviewRest/urls.py`: Rotas da API.

### Front-end (HTML, CSS, JavaScript Puro)
Localizado no diretório `front-end/`.
- `front-end/index.html`: A página principal da aplicação.
- `front-end/style.css`: Estilos CSS da aplicação.
- `front-end/js/api.js`: Funções para interagir com a API do back-end.
- `front-end/js/auth.js`: Funções relacionadas à autenticação do usuário.
- `front-end/js/restaurants.js`: Funções para exibir e gerenciar restaurantes no front-end.
- `front-end/js/review.js`: Funções para o gerenciamento de avaliações no front-end.
- `front-end/js/ui.js`: Funções para manipulação da interface do usuário.
- `front-end/js/app.js`: Lógica principal da aplicação front-end.

## Como Executar (Configuração Básica - Baseado na Estrutura)

Para um guia completo de execução, informações detalhadas sobre as dependências e o processo de configuração do ambiente seriam necessárias. No entanto, o fluxo geral seria:

### Back-end

1.  **Instalar dependências:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configurar o banco de dados:** (Assumindo SQLite por padrão, mas pode ser configurado em `ReviewRest/settings.py`)
    ```bash
    python manage.py migrate
    ```
3.  **Criar um superusuário (opcional, para acesso administrativo):**
    ```bash
    python manage.py createsuperuser
    ```
4.  **Iniciar o servidor Django:**
    ```bash
    python manage.py runserver
    ```

### Front-end

1.  Abra o arquivo `front-end/index.html` em seu navegador.
2.  Certifique-se de que o servidor back-end esteja rodando para que o front-end possa se comunicar com a API.

let currentUser = null;
let authToken = localStorage.getItem('authToken');

function storeToken(token) {
    localStorage.setItem('authToken', token);
    authToken = token;
}

function storeCurrentUser(user) {
    localStorage.setItem('currentUser', JSON.stringify(user));
    currentUser = user;
}

function clearTokenAndUser() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    authToken = null;
    currentUser = null;
}

function displayAuthError(viewId, error) {
    const errorElement = document.getElementById(`${viewId}-error`);
    if (errorElement) {
        let errorMessage = 'Ocorreu um erro.';
        if (error && error.data) {
            if (error.data.detail) {
                errorMessage = error.data.detail;
            } else if (typeof error.data === 'object') {
                errorMessage = Object.values(error.data).flat().join(' ');
            } else if (typeof error.data === 'string') {
                errorMessage = error.data;
            }
        } else if (error && error.message) {
            errorMessage = error.message;
        }
        errorElement.textContent = errorMessage;
        errorElement.style.display = 'block';
    }
}


async function loginUser(email, password) {
    clearErrorMessages();
    try {
        const response = await apiLogin(email, password);
        if (response && response.token && response.user) {
            storeToken(response.token);
            storeCurrentUser(response.user);
            updateNavOnLogin();
            showView('restaurants-list-view');
            if (typeof loadRestaurants === 'function') loadRestaurants();
            return true;
        } else {
            throw { data: { detail: "Resposta de login inválida do servidor." }};
        }
    } catch (error) {
        console.error('Login falhou:', error);
        displayAuthError('login', error);
        return false;
    }
}

async function registerUser(userData) {
    clearErrorMessages();
    try {
        const response = await apiRegister(userData);
        alert('Cadastro realizado com sucesso! Por favor, faça o login.');
        showView('login-view');
        document.getElementById('register-form').reset(); // Limpa o formulário de registro
        return true;
    } catch (error) {
        console.error('Cadastro falhou:', error);
        displayAuthError('register', error);
        return false;
    }
}

function logoutUser() {
    clearTokenAndUser();
    updateNavOnLogout();
    showView('login-view');
}

function checkLoginStatus() {
    authToken = localStorage.getItem('authToken');
    const storedUserString = localStorage.getItem('currentUser');
    
    if (authToken && storedUserString) {
        try {
            currentUser = JSON.parse(storedUserString);
            updateNavOnLogin();
            return true;
        } catch (e) {
            console.error("Erro ao parsear usuário do localStorage", e);
            logoutUser(); // Limpa estado inválido
            return false;
        }
    }
    updateNavOnLogout(); // Garante que a UI reflita o estado de logout
    return false;
}

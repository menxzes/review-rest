window.currentUser = null;
window.authToken = localStorage.getItem('authToken');

function storeToken(token) {
    localStorage.setItem('authToken', token);
    window.authToken = token; // Atualiza a variável global
}

function storeCurrentUser(user) {
    localStorage.setItem('currentUser', JSON.stringify(user));
    window.currentUser = user; // Atualiza a variável global
}

function clearTokenAndUser() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    window.authToken = null; // Limpa a variável global
    window.currentUser = null; // Limpa a variável global
}

function displayAuthError(viewId, error) {
    const errorElement = document.getElementById(`${viewId}-error`);
    if (errorElement) {
        let errorMessage = 'Ocorreu um erro.';
        if (error && error.data) {
            if (error.data.detail) {
                errorMessage = error.data.detail;
            } else if (typeof error.data === 'object') {
                // Tenta pegar a primeira mensagem de erro de validação
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
            updateNavOnLogin(); // Presumindo que updateNavOnLogin usa window.currentUser
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
        document.getElementById('register-form').reset();
        return true;
    } catch (error) {
        console.error('Cadastro falhou:', error);
        displayAuthError('register', error);
        return false;
    }
}

function logoutUser() {
    clearTokenAndUser();
    updateNavOnLogout(); // Presumindo que updateNavOnLogout usa window.currentUser
    showView('login-view');
}

function checkLoginStatus() {
    window.authToken = localStorage.getItem('authToken'); // Lê para a variável global
    const storedUserString = localStorage.getItem('currentUser');
    
    if (window.authToken && storedUserString) {
        try {
            window.currentUser = JSON.parse(storedUserString); // Parseia para a variável global
            updateNavOnLogin();
            return true;
        } catch (e) {
            console.error("Erro ao parsear usuário do localStorage", e);
            logoutUser(); // Limpa estado inválido
            return false;
        }
    }
    updateNavOnLogout();
    return false;
}

function clearErrorMessages() {
    document.querySelectorAll('.error-message').forEach(el => {
        el.textContent = '';
        el.style.display = 'none';
    });
}

function showView(viewId, skipAnimation = false) {
    document.querySelectorAll('.view').forEach(view => {
        view.style.display = 'none';
        if (!skipAnimation) {
            view.classList.remove('fadeInUp'); // Garante que a animação possa ser re-acionada
        }
    });

    const activeView = document.getElementById(viewId);
    if (activeView) {
        activeView.style.display = 'block';
        if (!skipAnimation) {
            // Força reflow para reiniciar a animação se a classe for readicionada rapidamente
            void activeView.offsetWidth; 
            activeView.classList.add('fadeInUp');
        }
    } else {
        console.error(`View com id ${viewId} não encontrada.`);
    }
    clearErrorMessages(); // Limpa erros ao mudar de view
}


function updateNavOnLogin() {
    document.querySelectorAll('.nav-guest').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.nav-user').forEach(el => el.style.display = 'inline-block');
    
    const userEmailSpan = document.getElementById('user-email');
    if (currentUser && userEmailSpan) {
        userEmailSpan.textContent = currentUser.email;
        if (currentUser.is_staff) {
            document.querySelectorAll('.nav-admin').forEach(el => el.style.display = 'inline-block');
        } else {
            document.querySelectorAll('.nav-admin').forEach(el => el.style.display = 'none');
        }
    } else if (userEmailSpan) {
        userEmailSpan.textContent = ''; // Limpa se não houver currentUser
    }
}

function updateNavOnLogout() {
    document.querySelectorAll('.nav-guest').forEach(el => el.style.display = 'inline-block');
    document.querySelectorAll('.nav-user').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.nav-admin').forEach(el => el.style.display = 'none');
    const userEmailSpan = document.getElementById('user-email');
    if(userEmailSpan) userEmailSpan.textContent = '';
}

function initializeUI() {
    if (checkLoginStatus()) { // checkLoginStatus já chama updateNav
        showView('restaurants-list-view', true); 
        if (typeof loadRestaurants === 'function') loadRestaurants();
    } else {
        showView('login-view', true);
    }
}

function showFormError(formId, message) {
    const errorElement = document.getElementById(`${formId}-error`);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function clearFormError(formId) {
    const errorElement = document.getElementById(`${formId}-error`);
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}
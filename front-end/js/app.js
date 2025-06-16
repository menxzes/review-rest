document.addEventListener('DOMContentLoaded', () => {
    // Listeners de Navegação
    document.getElementById('nav-home').addEventListener('click', (e) => {
        e.preventDefault();
        showView('restaurants-list-view');
        if (typeof loadRestaurants === 'function') loadRestaurants();
    });

    document.getElementById('nav-login').addEventListener('click', (e) => {
        e.preventDefault();
        showView('login-view');
        document.getElementById('login-form').reset();
        clearFormError('login-form');
    });

    document.getElementById('nav-register').addEventListener('click', (e) => {
        e.preventDefault();
        showView('register-view');
        document.getElementById('register-form').reset();
        clearFormError('register-form');
    });

    document.getElementById('nav-logout').addEventListener('click', (e) => {
        e.preventDefault();
        if (typeof logoutUser === 'function') logoutUser();
    });

    document.getElementById('nav-admin-restaurants').addEventListener('click', (e) => {
        e.preventDefault();
        if (currentUser && currentUser.is_staff) {
            showView('admin-restaurants-view');
            if (typeof loadAdminRestaurants === 'function') loadAdminRestaurants();
            closeRestaurantForm(); 
        } else {
            showView('login-view'); 
        }
    });


    // Listeners de Formulário
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        if (typeof loginUser === 'function') await loginUser(email, password);
    });

    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const userData = {
            nome: document.getElementById('register-nome').value,
            email: document.getElementById('register-email').value,
            password: document.getElementById('register-password').value,
            password2: document.getElementById('register-password2').value,
        };
        if (typeof registerUser === 'function') await registerUser(userData);
    });

    // O listener para 'add-review-form' já está em review.js

    // Listeners do Admin
    document.getElementById('show-add-restaurant-form').addEventListener('click', () => {
        if (typeof openAddRestaurantForm === 'function') openAddRestaurantForm();
    });
    
    document.getElementById('add-edit-restaurant-form').addEventListener('submit', async (e) => {
        if (typeof handleSaveRestaurant === 'function') await handleSaveRestaurant(e);
    });

    document.getElementById('cancel-edit-restaurant-button').addEventListener('click', () => {
        if (typeof closeRestaurantForm === 'function') closeRestaurantForm();
    });

    // Carregamento Inicial
    if (typeof initializeUI === 'function') initializeUI();
});
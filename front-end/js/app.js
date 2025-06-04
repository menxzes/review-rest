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
        document.getElementById('login-form').reset(); // Limpa form ao mostrar
        clearFormError('login-form');
    });

    document.getElementById('nav-register').addEventListener('click', (e) => {
        e.preventDefault();
        showView('register-view');
        document.getElementById('register-form').reset(); // Limpa form ao mostrar
        clearFormError('register-form');
    });

    document.getElementById('nav-logout').addEventListener('click', (e) => {
        e.preventDefault();
        if (typeof logoutUser === 'function') logoutUser();
    });

    const navAdminRestaurants = document.getElementById('nav-admin-restaurants');
    if (navAdminRestaurants) {
        navAdminRestaurants.addEventListener('click', (e) => {
            e.preventDefault();
            if (currentUser && currentUser.is_staff) {
                showView('admin-restaurants-view');
                if (typeof loadAdminRestaurants === 'function') loadAdminRestaurants();
                closeRestaurantForm(); // Garante que o form de add/edit esteja fechado inicialmente
            } else {
                showView('login-view'); // Se não for admin, vai para login
            }
        });
    }


    // Listeners de Formulário
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            if (typeof loginUser === 'function') await loginUser(email, password);
        });
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userData = {
                nome: document.getElementById('register-nome').value,
                email: document.getElementById('register-email').value,
                password: document.getElementById('register-password').value,
                password2: document.getElementById('register-password2').value,
            };
            if (typeof registerUser === 'function') await registerUser(userData);
        });
    }

    // O listener para 'add-review-form' já está em reviews.js para melhor encapsulamento.

    // Listeners do formulário de Admin de Restaurante
    const showAddRestaurantFormButton = document.getElementById('show-add-restaurant-form');
    if (showAddRestaurantFormButton) {
        showAddRestaurantFormButton.addEventListener('click', () => {
            if (typeof openAddRestaurantForm === 'function') openAddRestaurantForm();
        });
    }
    
    const addEditRestaurantForm = document.getElementById('add-edit-restaurant-form');
    if (addEditRestaurantForm) {
        addEditRestaurantForm.addEventListener('submit', async (e) => {
            // A função handleSaveRestaurant já tem e.preventDefault()
            if (typeof handleSaveRestaurant === 'function') await handleSaveRestaurant(e);
        });
    }

    const cancelEditRestaurantButton = document.getElementById('cancel-edit-restaurant-button');
    if (cancelEditRestaurantButton) {
        cancelEditRestaurantButton.addEventListener('click', () => {
            if (typeof closeRestaurantForm === 'function') closeRestaurantForm();
        });
    }

    // Carregamento Inicial
    if (typeof initializeUI === 'function') initializeUI();
});

async function loadRestaurants() {
    const container = document.getElementById('restaurants-container');
    container.innerHTML = '<p>Carregando restaurantes...</p>'; // Feedback de carregamento
    try {
        const restaurants = await apiGetRestaurants();
        container.innerHTML = ''; 
        if (!restaurants || restaurants.length === 0) {
            container.innerHTML = '<p>Nenhum restaurante encontrado.</p>';
            return;
        }
        restaurants.forEach(resto => {
            const div = document.createElement('div');
            div.className = 'restaurant-item';
            div.innerHTML = `
                <h3>${resto.nome}</h3>
                <p><strong>Culinária:</strong> ${resto.tipo_culinaria}</p>
                <p><strong>Endereço:</strong> ${resto.endereco}</p>
                <div class="button-group">
                    <button class="action-button-inline" onclick="viewRestaurantDetail(${resto.id})">Ver Detalhes & Avaliações</button>
                </div>
            `;
            container.appendChild(div);
        });
    } catch (error) {
        console.error('Falha ao carregar restaurantes:', error);
        container.innerHTML = `<p class="error-message" style="display:block;">Não foi possível carregar os restaurantes. ${error.data?.detail || error.message || ''}</p>`;
    }
}

async function viewRestaurantDetail(restaurantId) {
    showView('restaurant-detail-view'); 
    document.getElementById('restaurant-detail-name').textContent = 'Carregando...';
    document.getElementById('restaurant-detail-cuisine').textContent = '...';
    document.getElementById('restaurant-detail-address').textContent = '...';
    document.getElementById('restaurant-detail-phone').textContent = '...';
    document.getElementById('restaurant-detail-description').textContent = '...';
    document.getElementById('reviews-container').innerHTML = '<p>Carregando avaliações...</p>';


    try {
        const resto = await apiGetRestaurantById(restaurantId);
        document.getElementById('restaurant-detail-name').textContent = resto.nome;
        document.getElementById('restaurant-detail-cuisine').textContent = resto.tipo_culinaria;
        document.getElementById('restaurant-detail-address').textContent = resto.endereco;
        document.getElementById('restaurant-detail-phone').textContent = resto.telefone || 'Não informado';
        document.getElementById('restaurant-detail-description').textContent = resto.descricao || 'Nenhuma descrição disponível.';
        
        document.getElementById('review-restaurant-id').value = restaurantId;

        if (typeof loadReviewsForRestaurant === 'function') loadReviewsForRestaurant(restaurantId);

        const addReviewSection = document.getElementById('add-review-section');
        if (authToken && currentUser) {
             addReviewSection.style.display = 'block';
        } else {
             addReviewSection.style.display = 'none';
        }

    } catch (error) {
        console.error('Falha ao carregar detalhes do restaurante:', error);
        document.getElementById('restaurant-detail-name').textContent = "Erro ao Carregar";
        document.getElementById('reviews-container').innerHTML = `<p class="error-message" style="display:block;">Não foi possível carregar os detalhes. ${error.data?.detail || error.message || ''}</p>`;
    }
}

// --- Gerenciamento de Restaurantes pelo Admin ---
async function loadAdminRestaurants() {
    if (!currentUser || !currentUser.is_staff) {
        showView('login-view');
        return;
    }
    const listElement = document.getElementById('admin-restaurants-list');
    listElement.innerHTML = '<p>Carregando lista de restaurantes para administração...</p>';
    try {
        const restaurants = await apiGetRestaurants();
        listElement.innerHTML = '';
        if (!restaurants || restaurants.length === 0) {
            listElement.innerHTML = '<p>Nenhum restaurante cadastrado para gerenciar.</p>';
            return;
        }
        restaurants.forEach(resto => {
            const item = document.createElement('div');
            item.className = 'admin-restaurant-item';
            item.innerHTML = `
                <div>
                    <h4>${resto.nome}</h4>
                    <p>${resto.endereco} - ${resto.tipo_culinaria}</p>
                </div>
                <div class="button-group">
                    <button class="button-secundario" onclick="openEditRestaurantForm(${resto.id})">Editar</button>
                    <button class="delete-button" onclick="deleteRestaurant(${resto.id})">Deletar</button>
                </div>
            `;
            listElement.appendChild(item);
        });
    } catch (error) {
        console.error('Falha ao carregar restaurantes para admin:', error);
        listElement.innerHTML = `<p class="error-message" style="display:block;">Erro ao carregar restaurantes. ${error.data?.detail || error.message || ''}</p>`;
    }
}

function openAddRestaurantForm() {
    document.getElementById('form-restaurant-title').textContent = 'Adicionar Novo Restaurante';
    document.getElementById('restaurant-form-id').value = ''; 
    document.getElementById('add-edit-restaurant-form').reset();
    document.getElementById('save-restaurant-button').textContent = 'Adicionar Restaurante';
    document.getElementById('add-edit-restaurant-form').style.display = 'block';
    clearFormError('add-edit-restaurant-form');
}

async function openEditRestaurantForm(restaurantId) {
    clearFormError('add-edit-restaurant-form');
    try {
        const resto = await apiGetRestaurantById(restaurantId);
        document.getElementById('form-restaurant-title').textContent = `Editando: ${resto.nome}`;
        document.getElementById('restaurant-form-id').value = resto.id;
        document.getElementById('restaurant-form-name').value = resto.nome;
        document.getElementById('restaurant-form-address').value = resto.endereco;
        document.getElementById('restaurant-form-cuisine').value = resto.tipo_culinaria;
        document.getElementById('restaurant-form-phone').value = resto.telefone || '';
        document.getElementById('restaurant-form-description').value = resto.descricao || '';
        document.getElementById('save-restaurant-button').textContent = 'Atualizar Restaurante';
        document.getElementById('add-edit-restaurant-form').style.display = 'block';
    } catch (error) {
        console.error('Falha ao carregar restaurante para edição:', error);
        showFormError('admin-restaurants-view', `Não foi possível carregar dados para edição. ${error.data?.detail || error.message || ''}`);
    }
}

function closeRestaurantForm() {
    document.getElementById('add-edit-restaurant-form').style.display = 'none';
    document.getElementById('add-edit-restaurant-form').reset();
    clearFormError('add-edit-restaurant-form');
}


async function handleSaveRestaurant(event) {
    event.preventDefault();
    if (!authToken || !currentUser || !currentUser.is_staff) return;
    clearFormError('add-edit-restaurant-form');

    const restaurantId = document.getElementById('restaurant-form-id').value;
    const restaurantData = {
        nome: document.getElementById('restaurant-form-name').value,
        endereco: document.getElementById('restaurant-form-address').value,
        tipo_culinaria: document.getElementById('restaurant-form-cuisine').value,
        telefone: document.getElementById('restaurant-form-phone').value || null,
        descricao: document.getElementById('restaurant-form-description').value || null,
    };

    try {
        if (restaurantId) {
            await apiUpdateRestaurant(restaurantId, restaurantData, authToken);
        } else {
            await apiCreateRestaurant(restaurantData, authToken);
        }
        closeRestaurantForm();
        if (typeof loadAdminRestaurants === 'function') loadAdminRestaurants();
    } catch (error) {
        console.error('Falha ao salvar restaurante:', error);
        let errorMessage = "Falha ao salvar restaurante.";
        if (error.data) {
            errorMessage += " Detalhes: " + (error.data.detail || JSON.stringify(error.data));
        }
        showFormError('add-edit-restaurant-form', errorMessage);
    }
}

async function deleteRestaurant(restaurantId) {
    if (!authToken || !currentUser || !currentUser.is_staff) return;
    
    if (!confirm('Tem certeza que deseja deletar este restaurante? Esta ação não pode ser desfeita.')) return;

    try {
        await apiDeleteRestaurant(restaurantId, authToken);
        if (typeof loadAdminRestaurants === 'function') loadAdminRestaurants(); 
    } catch (error) {
        console.error('Falha ao deletar restaurante:', error);
        alert(`Falha ao deletar restaurante. ${error.data?.detail || error.message || ''}`);
    }
}
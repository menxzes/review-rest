const API_BASE_URL = 'http://127.0.0.1:8000/api';

async function request(endpoint, method = 'GET', data = null, token = null) {
    const config = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (token) {
        config.headers['Authorization'] = `Token ${token}`;
    }

    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        config.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        // --- MANTER ESTA LINHA PARA DEBUG ---
        const rawResponseText = await response.text();
        console.log(`[DEBUG - API Response] Endpoint: ${endpoint}, Status: ${response.status}, Raw Text:`, rawResponseText);
        // --- FIM DO DEBUG ---

        // --- CORREÇÃO AQUI: Restaurar o parseamento original do JSON ---
        let responseData;
        try {
            // Tenta parsear o JSON. Se não for JSON válido, isso lançará um erro.
            responseData = JSON.parse(rawResponseText);
        } catch (e) {
            // Se a resposta NÃO for JSON (ex: HTML de erro), tratamos como texto
            // Isso evita que 'responseData' se torne um objeto JSON inválido ou null silenciosamente
            responseData = rawResponseText; 
            console.warn(`[WARN - API Response] Resposta não é JSON válida para ${endpoint}.`);
        }
        // --- FIM DA CORREÇÃO ---


        if (!response.ok) {
            // Se a resposta não for OK (ex: 400, 401, 500), jogue um erro customizado.
            // A 'responseData' pode ser o objeto JSON do erro ou o texto bruto.
            const errorDetail = (typeof responseData === 'object' && responseData !== null && responseData.detail) 
                                ? responseData.detail 
                                : (typeof responseData === 'string' && responseData.length > 0 ? responseData : response.statusText);
            
            console.error('Erro na API:', response.status, errorDetail, responseData);
            throw { status: response.status, data: responseData || { detail: response.statusText } };
        }

        if (response.status === 204) { // No Content, como em um DELETE bem-sucedido
            return null;
        }
        
        return responseData; // Retorna o JSON parseado (se for um array, um objeto, etc.)
    } catch (error) {
        console.error('Erro no fetch ou processamento da resposta:', error);
        // Garante que o erro propagado tenha uma estrutura esperada
        if (error.status && error.data) {
            throw error;
        } else {
            throw { status: 'FETCH_ERROR', data: { detail: error.message || 'Erro de conexão ou rede.' } } ;
        }
    }
}

// === API de Usuário ===
const apiLogin = (email, password) => request('/users/login/', 'POST', { email, password });
const apiRegister = (userData) => request('/users/register/', 'POST', userData);

// === API de Restaurante ===
const apiGetRestaurants = () => request('/restaurants/');
const apiGetRestaurantById = (id) => request(`/restaurants/${id}/`);
const apiCreateRestaurant = (restaurantData, token) => request('/restaurants/', 'POST', restaurantData, token);
const apiUpdateRestaurant = (id, restaurantData, token) => request(`/restaurants/${id}/`, 'PUT', restaurantData, token);
const apiDeleteRestaurant = (id, token) => request(`/restaurants/${id}/`, 'DELETE', null, token);

// === API de Avaliação ===
const apiGetReviewsForRestaurant = (restaurantId) => request(`/reviews/?restaurant=${restaurantId}`);
const apiCreateReview = (reviewData, token) => request('/reviews/', 'POST', reviewData, token);
const apiUpdateReview = (id, reviewData, token) => request(`/reviews/${id}/`, 'PATCH', reviewData, token);
const apiDeleteReview = (id, token) => request(`/reviews/${id}/`, 'DELETE', null, token);
// === API de Perfil ===
const apiGetUserProfile = (token) => request('/users/profile/', 'GET', null, token);  
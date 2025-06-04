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
        
        const responseData = await response.json().catch(() => null); // Tenta parsear JSON, mas não falha se não houver corpo (ex: 204)

        if (!response.ok) {
            // Usa responseData se disponível, senão usa statusText
            const errorDetail = responseData && responseData.detail ? responseData.detail : (responseData ? responseData : response.statusText);
            console.error('Erro na API:', response.status, errorDetail, responseData);
            throw { status: response.status, data: responseData || { detail: response.statusText } };
        }

        if (response.status === 204) {
            return null;
        }
        return responseData;
    } catch (error) {
        console.error('Erro no fetch ou processamento da resposta:', error);
        // Garante que o erro propagado tenha uma estrutura esperada
        if (error.status && error.data) {
            throw error;
        } else {
            throw { status: 'FETCH_ERROR', data: { detail: error.message || 'Erro de conexão ou rede.' } };
        }
    }
}

// Chamadas da API de Usuário
const apiLogin = (email, password) => request('/users/login/', 'POST', { email, password });
const apiRegister = (userData) => request('/users/register/', 'POST', userData);

// Chamadas da API de Restaurante
const apiGetRestaurants = () => request('/restaurants/');
const apiGetRestaurantById = (id) => request(`/restaurants/${id}/`);
const apiCreateRestaurant = (restaurantData, token) => request('/restaurants/', 'POST', restaurantData, token);
const apiUpdateRestaurant = (id, restaurantData, token) => request(`/restaurants/${id}/`, 'PUT', restaurantData, token);
const apiDeleteRestaurant = (id, token) => request(`/restaurants/${id}/`, 'DELETE', null, token);

// Chamadas da API de Avaliação
const apiGetReviews = () => request('/reviews/'); // Para todas as avaliações, se necessário
const apiGetReviewsForRestaurant = (restaurantId) => request(`/reviews/?restaurante=${restaurantId}`);
const apiCreateReview = (reviewData, token) => request('/reviews/', 'POST', reviewData, token);
const apiUpdateReview = (id, reviewData, token) => request(`/reviews/${id}/`, 'PATCH', reviewData, token);
const apiDeleteReview = (id, token) => request(`/reviews/${id}/`, 'DELETE', null, token);

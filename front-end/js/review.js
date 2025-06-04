async function loadReviewsForRestaurant(restaurantId) {
    const container = document.getElementById('reviews-container');
    container.innerHTML = '<p>Carregando avaliações...</p>';
    try {
        const reviews = await apiGetReviewsForRestaurant(restaurantId);
        container.innerHTML = ''; 
        if (!reviews || reviews.length === 0) {
            container.innerHTML = '<p>Nenhuma avaliação ainda. Seja o primeiro!</p>';
            return;
        }
        reviews.forEach(review => {
            const div = document.createElement('div');
            div.className = 'review-item';
            
            const userName = review.usuario ? review.usuario.nome : 'Usuário Anônimo';
            const userEmail = review.usuario ? review.usuario.email : null;
            const reviewDate = new Date(review.data_avaliacao).toLocaleDateString('pt-BR', {
                day: '2-digit', month: 'long', year: 'numeric'
            });

            let editDeleteButtons = '';
            if (currentUser && ( (userEmail && currentUser.email === userEmail) || currentUser.is_staff) ) {
                 editDeleteButtons = `
                    <div class="button-group">
                        <button class="button-secundario" style="font-size:0.8em; padding: 0.4em 0.8em;" onclick="openEditReviewForm(${review.id}, ${review.restaurante}, ${review.nota}, '${review.comentario.replace(/'/g, "\\'")}')">Editar</button>
                        <button class="delete-button" style="font-size:0.8em; padding: 0.4em 0.8em;" onclick="deleteReview(${review.id}, ${review.restaurante})">Deletar</button>
                    </div>
                `;
            }

            div.innerHTML = `
                <h4>Nota: ${'★'.repeat(review.nota)}${'☆'.repeat(5-review.nota)} (${review.nota}/5)</h4> 
                <p><strong>${userName}</strong></p>
                <p class="review-date">Em ${reviewDate}</p>
                <p>${review.comentario}</p>
                ${editDeleteButtons}
            `;
            container.appendChild(div);
        });
    } catch (error) {
        console.error('Falha ao carregar avaliações:', error);
        container.innerHTML = `<p class="error-message" style="display:block;">Não foi possível carregar as avaliações. ${error.data?.detail || error.message || ''}</p>`;
    }
}

async function handleAddOrUpdateReview(event) {
    event.preventDefault();
    if (!authToken || !currentUser) return;
    clearFormError('add-review-form'); // Limpa erro do formulário de avaliação

    // Determina se é uma edição ou nova avaliação pelo ID no formulário de edição (se existir)
    // Este handler é genérico, mas o formulário de edição precisaria ser separado ou mais complexo.
    // Para simplificar, vamos focar no handleAddReview e o openEditReviewForm usará prompts.

    const restaurantId = document.getElementById('review-restaurant-id').value; // Usado para recarregar
    const reviewIdToUpdate = document.getElementById('update-review-id') ? document.getElementById('update-review-id').value : null;


    const reviewData = {
        restaurante: parseInt(document.getElementById('review-restaurant-id').value), // Sempre necessário
        nota: parseInt(document.getElementById('review-rating').value),
        comentario: document.getElementById('review-comment').value,
    };
    
    // Validação básica no frontend
    if (isNaN(reviewData.nota) || reviewData.nota < 1 || reviewData.nota > 5) {
        showFormError('add-review-form', 'A nota deve ser entre 1 e 5.');
        return;
    }
    if (!reviewData.comentario.trim()) {
        showFormError('add-review-form', 'O comentário não pode estar vazio.');
        return;
    }


    try {
        if (reviewIdToUpdate) { // Lógica de atualização (se tivéssemos um formulário de edição dedicado)
            await apiUpdateReview(reviewIdToUpdate, reviewData, authToken);
            // Ocultar formulário de edição, etc.
        } else { // Nova avaliação
            await apiCreateReview(reviewData, authToken);
            document.getElementById('add-review-form').reset();
        }
        if (typeof loadReviewsForRestaurant === 'function') loadReviewsForRestaurant(reviewData.restaurante);
    } catch (error) {
        console.error('Falha ao enviar/atualizar avaliação:', error);
        let errorMessage = "Falha ao enviar avaliação.";
        if (error.data) {
             errorMessage = error.data.detail || (error.data.non_field_errors ? error.data.non_field_errors.join(' ') : JSON.stringify(error.data));
        }
        showFormError('add-review-form', errorMessage);
    }
}


// Função separada para o formulário de adicionar avaliação
const addReviewFormElement = document.getElementById('add-review-form');
if (addReviewFormElement) {
    addReviewFormElement.addEventListener('submit', handleAddOrUpdateReview);
}


function openEditReviewForm(reviewId, restaurantId, currentRating, currentComment) {
    // Usando prompts para simplicidade. Uma UI real teria um modal/formulário.
    const newRatingStr = prompt("Nova nota (1-5):", currentRating);
    if (newRatingStr === null) return; // Cancelado
    const newRating = parseInt(newRatingStr);

    const newComment = prompt("Novo comentário:", currentComment);
    if (newComment === null) return; // Cancelado

    if (isNaN(newRating) || newRating < 1 || newRating > 5) {
        alert("Nota inválida. Deve ser entre 1 e 5.");
        return;
    }
    if (newComment.trim() === "") {
        alert("O comentário não pode estar vazio.");
        return;
    }

    const reviewData = {
        nota: newRating,
        comentario: newComment,
        restaurante: parseInt(restaurantId) // O backend pode precisar disso para validação ou contexto
    };
    updateReview(reviewId, parseInt(restaurantId), reviewData);
}


async function updateReview(reviewId, restaurantIdToReload, reviewData) {
    if (!authToken || !currentUser) return;
    try {
        await apiUpdateReview(reviewId, reviewData, authToken);
        if (typeof loadReviewsForRestaurant === 'function') loadReviewsForRestaurant(restaurantIdToReload);
    } catch (error) {
        console.error('Falha ao atualizar avaliação:', error);
        alert(`Falha ao atualizar avaliação: ${error.data?.detail || JSON.stringify(error.data)}`);
    }
}

async function deleteReview(reviewId, restaurantIdToReload) {
    if (!authToken || !currentUser) return;
    
    if (!confirm('Tem certeza que deseja deletar esta avaliação?')) return;
    try {
        await apiDeleteReview(reviewId, authToken);
        if (typeof loadReviewsForRestaurant === 'function') loadReviewsForRestaurant(restaurantIdToReload);
    } catch (error) {
        console.error('Falha ao deletar avaliação:', error);
        alert(`Falha ao deletar avaliação. ${error.data?.detail || error.message || ''}`);
    }
}

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
            
            // O campo no review.usuario para o nome do usuário agora deve ser user.nome ou user.email
            const userName = review.user ? review.user.nome : 'Usuário Anônimo'; 
            const userEmail = review.user ? review.user.email : null; 
            
            const reviewDate = new Date(review.date).toLocaleDateString('pt-BR', { 
                day: '2-digit', month: 'long', year: 'numeric'
            });

            let editDeleteButtons = '';
            if (window.currentUser && ( (userEmail && window.currentUser.email === userEmail) || window.currentUser.is_staff) ) {
                 editDeleteButtons = `
                    <div class="button-group">
                        <button class="button-secundario" style="font-size:0.8em; padding: 0.4em 0.8em;" onclick="openEditReviewForm(${review.id}, ${review.restaurant}, ${review.rating}, '${review.comment.replace(/'/g, "\\'")}')">Editar</button> # Corrigido: review.restaurante, review.nota, review.comentario
                        <button class="delete-button" style="font-size:0.8em; padding: 0.4em 0.8em;" onclick="deleteReview(${review.id}, ${review.restaurant})">Deletar</button> # Corrigido: review.restaurante
                    </div>
                `;
            }

            div.innerHTML = `
                <h4>Nota: ${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)} (${review.rating}/5)</h4> 
                <p><strong>${userName}</strong></p>
                <p class="review-date">Em ${reviewDate}</p>
                <p>${review.comment}</p> # Corrigido: review.comentario para review.comment
                ${editDeleteButtons}
            `;
            container.appendChild(div);
        });
    } catch (error) {
        console.error('Falha ao carregar avaliações:', error);
        container.innerHTML = `<p class="error-message" style="display:block;">Não foi possível carregar as avaliações. ${error.data?.detail || error.message || ''}</p>`;
    }
}

async function handleAddReview(event) {
    event.preventDefault();
    if (!window.authToken || !window.currentUser) {
        console.warn("Tentativa de adicionar avaliação sem usuário logado ou token.");
        alert("Você precisa estar logado para enviar uma avaliação.");
        return;
    }
    clearFormError('add-review-form');

    const restaurantId = document.getElementById('review-restaurant-id').value;
    const reviewData = {
        restaurant: parseInt(restaurantId),
        rating: parseInt(document.getElementById('review-rating').value),
        comment: document.getElementById('review-comment').value,
    };
    
    if (isNaN(reviewData.rating) || reviewData.rating < 1 || reviewData.rating > 5) {
        showFormError('add-review-form', 'A nota deve ser entre 1 e 5.');
        return;
    }
    if (!reviewData.comment.trim()) {
        showFormError('add-review-form', 'O comentário não pode estar vazio.');
        return;
    }

    try {
        await apiCreateReview(reviewData, window.authToken);
        document.getElementById('add-review-form').reset();
        if (typeof loadReviewsForRestaurant === 'function') loadReviewsForRestaurant(restaurantId);
    } catch (error) {
        console.error('Falha ao enviar avaliação:', error);
        let errorMessage = "Falha ao enviar avaliação.";
        if (error.data) {
             errorMessage = error.data.detail || (error.data.non_field_errors ? error.data.non_field_errors.join(' ') : JSON.stringify(error.data));
             if (error.data.rating) errorMessage += ` Nota: ${error.data.rating.join(' ')}`;
             if (error.data.comment) errorMessage += ` Comentário: ${error.data.comment.join(' ')}`;
             // Certifique-se de que a mensagem de erro para o restaurante duplicado também é tratada
             if (error.data.non_field_errors && error.data.non_field_errors.includes("Você já avaliou este restaurante.")) {
                 errorMessage = "Você já avaliou este restaurante.";
             }
        }
        showFormError('add-review-form', errorMessage);
    }
}

// O listener de submit para o formulário de add-review
const addReviewFormElement = document.getElementById('add-review-form');
if (addReviewFormElement) {
    addReviewFormElement.addEventListener('submit', handleAddReview);
}



function openEditReviewForm(reviewId, restaurantId, currentRating, currentComment) {
    const newRatingStr = prompt("Nova nota (1-5):", currentRating);
    if (newRatingStr === null) return; 
    const newRating = parseInt(newRatingStr);

    const newComment = prompt("Novo comentário:", currentComment);
    if (newComment === null) return; 

    if (isNaN(newRating) || newRating < 1 || newRating > 5) {
        alert("Nota inválida. Deve ser entre 1 e 5.");
        return;
    }
    if (newComment.trim() === "") {
        alert("O comentário não pode estar vazio.");
        return;
    }

    const reviewData = {
        rating: newRating, 
        comment: newComment, 
    };
    updateReview(reviewId, parseInt(restaurantId), reviewData);
}


async function updateReview(reviewId, restaurantIdToReload, reviewData) {
    if (!window.authToken || !window.currentUser) {
        alert("Você precisa estar logado para atualizar uma avaliação.");
        return;
    }
    try {
        await apiUpdateReview(reviewId, reviewData, window.authToken);
        if (typeof loadReviewsForRestaurant === 'function') loadReviewsForRestaurant(restaurantIdToReload);
    } catch (error) {
        console.error('Falha ao atualizar avaliação:', error);
        alert(`Falha ao atualizar avaliação: ${error.data?.detail || JSON.stringify(error.data)}`);
    }
}

async function deleteReview(reviewId, restaurantIdToReload) {
    if (!window.authToken || !window.currentUser) {
        alert("Você precisa estar logado para deletar uma avaliação.");
        return;
    }
    
    if (!confirm('Tem certeza que deseja deletar esta avaliação?')) return;
    try {
        await apiDeleteReview(reviewId, window.authToken);
        if (typeof loadReviewsForRestaurant === 'function') loadReviewsForRestaurant(restaurantIdToReload);
    } catch (error) {
        console.error('Falha ao deletar avaliação:', error);
        alert(`Falha ao deletar avaliação. ${error.data?.detail || error.message || ''}`);
    }
}
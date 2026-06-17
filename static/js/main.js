function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showNotification(message, type = 'success') {
    const container = document.getElementById('notification-container');
    if (!container) return;

    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show toast-custom`;
    alert.role = 'alert';
    alert.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`;

    container.appendChild(alert);

    setTimeout(() => {
        if (alert) {
            alert.classList.remove('show');
            alert.classList.add('hide');
            setTimeout(() => alert.remove(), 400);
        }
    }, 4500);
}

function renderProducts(products) {
    const grid = document.getElementById('product-grid');
    if (!grid) return;

    grid.innerHTML = '';
    if (!products.length) {
        grid.innerHTML = '<div class="col-12"><div class="alert alert-info">Товары не найдены по заданным параметрам.</div></div>';
        return;
    }

    products.forEach((product) => {
        const card = document.createElement('div');
        card.className = 'col-sm-6 col-md-4';
        card.innerHTML = `
            <div class="card h-100">
                <img src="${product.фото_товара || '/static/images/default-boardgame.svg'}" class="product-image" alt="${product.название}">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${product.название}</h5>
                    <p class="card-text text-muted small flex-grow-1">${product.описание ? product.описание.substring(0, 80) + '...' : ''}</p>
                    <div class="mb-2">
                        <span class="badge bg-primary">${product.категория.название}</span>
                        <span class="badge bg-secondary">${product.производитель.название}</span>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-auto mb-3">
                        <span class="fs-6 fw-bold text-primary">${product.цена} ₽</span>
                        <small class="text-muted">${product.количество_на_складе} шт.</small>
                    </div>
                    <div class="d-grid gap-2">
                        <a href="/catalog/${product.id}/" class="btn btn-outline-primary btn-sm">Подробнее</a>
                        <button class="btn btn-primary btn-sm" onclick="addToCart(${product.id})">
                            В корзину
                        </button>
                    </div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function setLoading(isLoading) {
    const spinner = document.getElementById('loading-spinner');
    if (!spinner) return;
    spinner.style.display = isLoading ? 'block' : 'none';
}

async function loadProducts(page = 1) {
    const category = document.getElementById('category')?.value || '';
    const manufacturer = document.getElementById('manufacturer')?.value || '';
    const search = document.getElementById('search')?.value || '';

    const params = new URLSearchParams();
    if (page) params.append('page', page);
    if (category) params.append('category', category);
    if (manufacturer) params.append('manufacturer', manufacturer);
    if (search) params.append('search', search);

    const url = `/api/products/?${params.toString()}`;
    setLoading(true);

    try {
        const response = await fetch(url, {
            headers: {
                'Accept': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error('Ошибка загрузки товаров');
        }
        const data = await response.json();
        renderProducts(data.results || data);
    } catch (error) {
        showNotification('Не удалось загрузить товары. Попробуйте позже.', 'danger');
    } finally {
        setLoading(false);
    }
}

async function addToCart(productId) {
    setLoading(true);
    const csrfToken = getCookie('csrftoken');
    try {
        const response = await fetch('/api/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ product_id: productId, quantity: 1 }),
        });

        if (!response.ok) {
            const data = await response.json();
            const error = data.detail || 'Не удалось добавить товар в корзину.';
            throw new Error(error);
        }
        showNotification('Товар добавлен в корзину.', 'success');
    } catch (error) {
        showNotification(error.message, 'danger');
    } finally {
        setLoading(false);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('product-grid')) {
        loadProducts();
    }

    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', (event) => {
            event.preventDefault();
            loadProducts();
        });
    }
});

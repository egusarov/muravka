document.addEventListener('DOMContentLoaded', () => {

    const UI_ANIMATION_DELAY = 200;
    const BUTTON_RESET_DELAY = 800;

    const headerCounter = document.querySelector('.cart-counter');

    // ======================
    // CSRF helper
    // ======================
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }

    // ======================
    // UNIVERSAL FETCH
    // ======================
    async function sendRequest(url, formData) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: formData
            });

            if (!response.ok) {
                console.error('Request failed:', response.status);
                throw new Error();
            }

            return await response.json();

        } catch (error) {
            return null;
        }
    }

    // ======================
    // ADD TO CART
    // ======================
    document.querySelectorAll('.js-add-to-cart').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const button = form.querySelector('[type="submit"]');
            const formData = new FormData(form);
            const originalHTML = button.innerHTML;

            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm text-light"></span>';

            const data = await sendRequest(form.action, formData);

            // fallback
            if (!data) {
                button.innerHTML = originalHTML;
                button.disabled = false;
                form.submit();
                return;
            }

            if (data.success) {

                // 👉 Analytics
                if (window.Analytics) {
                    Analytics.addToCart({
                        id: form.dataset.productId,
                        name: form.dataset.productName,
                        price: Number(form.dataset.productPrice) || 0,
                        quantity: 1
                    });
                }

                // 👉 UI
                if (headerCounter) {
                    headerCounter.textContent = data.cart_count;
                    headerCounter.style.display =
                        data.cart_count > 0 ? 'inline-block' : 'none';

                    headerCounter.classList.add('bump');
                    setTimeout(() => headerCounter.classList.remove('bump'), UI_ANIMATION_DELAY);
                }

                button.innerHTML = '✓';
            }

            setTimeout(() => {
                button.innerHTML = originalHTML;
                button.disabled = false;
            }, BUTTON_RESET_DELAY);
        });
    });

    // ======================
    // CART PAGE
    // ======================
    const totalEl = document.getElementById('cart-total');

    document.querySelectorAll('.cart-item').forEach(item => {

        const forms = item.querySelectorAll('.js-cart-form');
        const quantityEl = item.querySelector('.cart-quantity-value');
        const minusBtn = item.querySelector('.js-decrease-btn');

        forms.forEach(form => {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const formData = new FormData(form);
                const quantityChange = parseInt(formData.get('quantity')) || 0;

                const data = await sendRequest(form.action, formData);

                if (!data) {
                    form.submit();
                    return;
                }

                const isRemove = form.classList.contains('js-remove-form');

                if (isRemove) {
                    item.style.opacity = '0';
                    setTimeout(() => item.remove(), UI_ANIMATION_DELAY);
                } else {
                    let currentQty = parseInt(quantityEl.textContent) || 0;
                    currentQty += quantityChange;

                    if (currentQty <= 0) {
                        item.remove();
                    } else {
                        quantityEl.textContent = currentQty;

                        if (minusBtn) {
                            minusBtn.disabled = currentQty <= 1;
                        }
                    }
                }

                // TOTAL
                if (totalEl) {
                    totalEl.textContent = Math.round(data.cart_total);

                    totalEl.classList.add('bump');
                    setTimeout(() => totalEl.classList.remove('bump'), UI_ANIMATION_DELAY);
                }

                // HEADER COUNTER
                if (headerCounter) {
                    headerCounter.textContent = data.cart_count;

                    headerCounter.style.display =
                        data.cart_count > 0 ? 'inline-block' : 'none';

                    headerCounter.classList.add('bump');
                    setTimeout(() => headerCounter.classList.remove('bump'), UI_ANIMATION_DELAY);
                }

                // EMPTY CART
                if (data.cart_count === 0) {
                    location.reload();
                }
            });
        });

    });

});
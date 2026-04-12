document.addEventListener('DOMContentLoaded', () => {

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

            if (!response.ok) throw new Error();

            return await response.json();

        } catch (error) {
            return null;
        }
    }

    // ======================
    // ADD TO CART (catalog)
    // ======================
    const addForms = document.querySelectorAll('.js-add-to-cart');

    addForms.forEach(form => {
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

            // success
            if (data.success) {
                const counter = document.querySelector('.cart-counter');

                if (counter) {
                    counter.textContent = data.cart_count;

                    counter.style.display =
                        data.cart_count > 0 ? 'inline-block' : 'none';

                    counter.classList.add('bump');
                    setTimeout(() => counter.classList.remove('bump'), 200);
                }

                button.innerHTML = '✓';

                if (typeof gtag !== 'undefined') {
                    gtag('event', 'add_to_cart', {
                        currency: 'UAH',
                        value: parseFloat(form.dataset.productPrice) || 0,
                        items: [{
                            item_id: form.dataset.productId,
                            item_name: form.dataset.productName,
                            price: parseFloat(form.dataset.productPrice) || 0,
                            quantity: 1
                        }]
                    });
                }
            }

            setTimeout(() => {
                button.innerHTML = originalHTML;
                button.disabled = false;
            }, 800);
        });
    });

    // ======================
    // CART PAGE
    // ======================

    // GLOBAL UI
    const totalEl = document.getElementById('cart-total');
    const counter = document.querySelector('.cart-counter');

    // CART ITEMS
    const cartItems = document.querySelectorAll('.cart-item');

    cartItems.forEach(item => {

        const forms = item.querySelectorAll('.js-cart-form');

        const quantityEl = item.querySelector('.cart-quantity-value');
        const minusBtn = item.querySelector('.js-decrease-btn');

        forms.forEach(form => {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const formData = new FormData(form);
                const quantityChange = parseInt(formData.get('quantity')) || 0;

                const data = await sendRequest(form.action, formData);

                // fallback
                if (!data) {
                    form.submit();
                    return;
                }

                // REMOVE
                const isRemove = form.classList.contains('js-remove-form');

                if (isRemove) {
                    item.style.opacity = '0';
                    setTimeout(() => item.remove(), 200);
                } else {
                    let currentQty = parseInt(quantityEl.textContent);
                    currentQty += quantityChange;

                    if (currentQty <= 0) {
                        item.remove();
                    } else {
                        quantityEl.textContent = currentQty;

                        // ✅ фикс бага с кнопкой "-"
                        if (minusBtn) {
                            minusBtn.disabled = currentQty <= 1;
                        }
                    }
                }

                // TOTAL
                if (totalEl) {
                    totalEl.textContent = Math.round(data.cart_total);

                    totalEl.classList.add('bump');
                    setTimeout(() => totalEl.classList.remove('bump'), 200);
                }

                // HEADER COUNTER
                if (counter) {
                    counter.textContent = data.cart_count;

                    counter.style.display =
                        data.cart_count > 0 ? 'inline-block' : 'none';

                    counter.classList.add('bump');
                    setTimeout(() => counter.classList.remove('bump'), 200);
                }

                // EMPTY CART
                if (data.cart_count === 0) {
                    location.reload();
                }
            });
        });

    });

});
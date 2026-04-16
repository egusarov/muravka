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
                    let currentQty = parseInt(quantityEl.textContent) || 0;
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

    // ======================
    // SOCIAL TRACKING
    // ======================

    const socialLinks = document.querySelectorAll('.js-social-click');

    socialLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const url = link.href;

            if (typeof gtag !== 'undefined') {
                e.preventDefault();

                gtag('event', 'social_click', {
                    social_network: link.dataset.social,
                    location: link.dataset.location,
                    event_callback: () => {
                        window.location.href = url;
                    }
                });

                // fallback если callback не сработает
                setTimeout(() => {
                    window.location.href = url;
                }, 300);
            }
        });
    });

    // CTA TRACKING
    document.querySelectorAll('.js-cta-click').forEach(btn => {
        btn.addEventListener('click', () => {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'cta_click', {
                    location: btn.dataset.location || 'unknown',
                    cta: btn.dataset.cta
                });
            }
        });
    });

    // ADD TO CART TRACKING
    document.querySelectorAll('.js-add-to-cart').forEach(form => {
        form.addEventListener('submit', function (e) {
            if (typeof gtag === 'undefined') return;

            e.preventDefault();

            const productId = form.dataset.productId;
            const productName = form.dataset.productName;
            const price = parseFloat(form.dataset.productPrice) || 0;
            const quantity = parseInt(form.querySelector('input[name="quantity"]').value) || 1;

            let submitted = false;

            const submitForm = () => {
                if (submitted) return;
                submitted = true;
                form.submit();
            };

            gtag('event', 'add_to_cart', {
                currency: 'UAH',
                value: price * quantity,
                items: [
                    {
                        item_id: productId,
                        item_name: productName,
                        price: price,
                        quantity: quantity
                    }
                ],
                event_callback: submitForm
            });

            // fallback (если GA не ответит)
            setTimeout(submitForm, 300);
        });
    });

    // PRODUCT DETAIL tracking
    const detail = document.querySelector('.product-detail-page');

    if (detail && typeof gtag !== 'undefined') {
        gtag('event', 'view_item', {
            currency: 'UAH',
            value: parseFloat(detail.dataset.productPrice),
            items: [{
                item_id: detail.dataset.productId,
                item_name: detail.dataset.productName,
                price: parseFloat(detail.dataset.productPrice)
            }]
        });
    }

    // CHECKOUT tracking
    const checkout = document.querySelector('.checkout-page');

    if (checkout && typeof gtag !== 'undefined') {
        const items = [];

        document.querySelectorAll('.checkout-item').forEach(el => {
            items.push({
                item_id: el.dataset.productId,
                item_name: el.dataset.productName,
                price: parseFloat(el.dataset.productPrice) || 0,
                quantity: parseInt(el.dataset.productQuantity, 10)
            });
        });

        if (items.length === 0) return;

        gtag('event', 'begin_checkout', {
            currency: 'UAH',
            value: parseFloat(checkout.dataset.total),
            items: items
        });
    }

    // PURCHASE tracking
    const orderPage = document.querySelector('.order-created-page');

    if (orderPage && typeof gtag !== 'undefined') {
        const items = [];

        orderPage.querySelectorAll('.purchase-item').forEach(el => {
            items.push({
                item_id: el.dataset.productId,
                item_name: el.dataset.productName,
                price: parseFloat(el.dataset.productPrice) || 0,
                quantity: parseInt(el.dataset.productQuantity, 10) || 1
            });
        });

        if (items.length === 0) return;

        const transactionId = orderPage.dataset.transactionId;

        if (sessionStorage.getItem('purchase_' + transactionId)) return;

        sessionStorage.setItem('purchase_' + transactionId, '1');

        gtag('event', 'purchase', {
            transaction_id: orderPage.dataset.transactionId,
            currency: 'UAH',
            value: parseFloat(orderPage.dataset.total) || 0,
            items: items,

            // UTM
            utm_source: orderPage.dataset.utmSource || 'direct',
            utm_medium: orderPage.dataset.utmMedium || 'none',
            utm_campaign: orderPage.dataset.utmCampaign || 'none'
        });
    }

});
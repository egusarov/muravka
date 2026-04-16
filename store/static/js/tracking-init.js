document.addEventListener('DOMContentLoaded', () => {

    if (!window.Analytics) return;

    // ======================
    // SOCIAL CLICK
    // ======================
    const socialLinks = document.querySelectorAll('.js-social-click');

    socialLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const url = link.href;
            const isBlank = link.target === '_blank';

            e.preventDefault();

            const navigate = () => {
                if (isBlank) {
                    window.open(url, '_blank', 'noopener,noreferrer');
                } else {
                    window.location.href = url;
                }
            };

            Analytics.socialClick({
                network: link.dataset.social,
                location: link.dataset.location
            }, navigate);
        });
    });

    // ======================
    // CTA CLICK
    // ======================
    document.querySelectorAll('.js-cta-click').forEach(btn => {
        btn.addEventListener('click', () => {
            Analytics.ctaClick({
                location: btn.dataset.location || 'unknown',
                cta: btn.dataset.cta || 'unknown'
            });
        });
    });

    // ======================
    // PRODUCT DETAIL
    // ======================
    const detail = document.querySelector('.product-detail-page');

    if (detail) {
        Analytics.viewItem({
            id: detail.dataset.productId,
            name: detail.dataset.productName,
            price: Number(detail.dataset.productPrice) || 0
        });
    }

    // ======================
    // CHECKOUT
    // ======================
    const checkout = document.querySelector('.checkout-page');

    if (checkout) {
        const items = [];

        document.querySelectorAll('.checkout-item').forEach(el => {
            items.push({
                item_id: el.dataset.productId,
                item_name: el.dataset.productName,
                price: Number(el.dataset.productPrice) || 0,
                quantity: parseInt(el.dataset.productQuantity, 10) || 1
            });
        });

        if (items.length > 0) {
            Analytics.beginCheckout({
                value: Number(checkout.dataset.total) || 0,
                items
            });
        }
    }

    // ======================
    // PURCHASE
    // ======================
    const orderPage = document.querySelector('.order-created-page');

    if (orderPage) {
        const items = [];

        orderPage.querySelectorAll('.purchase-item').forEach(el => {
            items.push({
                item_id: el.dataset.productId,
                item_name: el.dataset.productName,
                price: Number(el.dataset.productPrice) || 0,
                quantity: parseInt(el.dataset.productQuantity, 10) || 1
            });
        });

        if (items.length === 0) return;

        const transactionId = orderPage.dataset.transactionId;

        // защита от дублей
        if (sessionStorage.getItem('purchase_' + transactionId)) return;

        sessionStorage.setItem('purchase_' + transactionId, '1');

        Analytics.purchase({
            transactionId,
            value: Number(orderPage.dataset.total) || 0,
            items,
            utm: {
                utm_source: orderPage.dataset.utmSource || 'direct',
                utm_medium: orderPage.dataset.utmMedium || 'none',
                utm_campaign: orderPage.dataset.utmCampaign || 'none'
            }
        });
    }

});
window.Analytics = (function () {

    const DEBUG = false;

    function isAvailable() {
        return typeof gtag !== 'undefined';
    }

    function track(eventName, payload = {}, options = {}) {

        if (DEBUG) {
            console.log('[Analytics]', eventName, payload);
        }

        if (!isAvailable()) {
            if (options.callback) {
                setTimeout(options.callback, 0);
            }
            return;
        }

        let called = false;

        const callback = () => {
            if (called) return;
            called = true;

            if (options.callback) {
                options.callback();
            }
        };

        gtag('event', eventName, {
            ...payload,
            event_callback: callback
        });

        // fallback
        setTimeout(callback, options.timeout || 300);
    }

    // ======================
    // ECOMMERCE
    // ======================

    function addToCart({ id, name, price, quantity = 1 }) {
        track('add_to_cart', {
            currency: 'UAH',
            value: price * quantity,
            items: [{
                item_id: id,
                item_name: name,
                price: price,
                quantity: quantity
            }]
        });
    }

    function viewItem({ id, name, price }) {
        track('view_item', {
            currency: 'UAH',
            value: price,
            items: [{
                item_id: id,
                item_name: name,
                price: price
            }]
        });
    }

    function beginCheckout({ value, items }) {
        track('begin_checkout', {
            currency: 'UAH',
            value,
            items
        });
    }

    function purchase({ transactionId, value, items, utm = {} }) {
        track('purchase', {
            transaction_id: transactionId,
            currency: 'UAH',
            value,
            items,
            ...utm
        });
    }

    // ======================
    // MARKETING
    // ======================

    function socialClick({ network, location }, callback) {
        track('social_click', {
            social_network: network,
            location
        }, { callback });
    }

    function ctaClick({ location, cta }) {
        track('cta_click', {
            location,
            cta
        });
    }

    return {
        addToCart,
        viewItem,
        beginCheckout,
        purchase,
        socialClick,
        ctaClick
    };

})();
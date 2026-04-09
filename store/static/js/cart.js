document.addEventListener('DOMContentLoaded', () => {

    const forms = document.querySelectorAll('.js-add-to-cart');

    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const button = form.querySelector('[type="submit"]');
            const url = form.action;
            const formData = new FormData(form);

            // 👉 UX: блокируем кнопку
            button.disabled = true;
            const originalText = button.textContent;
            button.textContent = 'Добавляем...';

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    // 👉 обновляем счетчик корзины
                    const counter = document.querySelector('.cart-counter');
                    if (counter) {
                        counter.textContent = data.cart_count;

                        // 👉 показать если был скрыт
                        if (data.cart_count > 0) {
                            counter.style.display = 'inline-block';
                        } else {
                            counter.style.display = 'none';
                        }

                        // 👉 bump animation
                        counter.classList.add('bump');
                        setTimeout(() => {
                            counter.classList.remove('bump');
                        }, 200);
                    }

                    // 👉 UX feedback
                    button.textContent = '✓ Добавлено';

                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 1200);
                }

            } catch (error) {
                console.error('Ошибка:', error);

                // 👉 fallback если что-то сломалось
                form.submit();
            }
        });
    });

});
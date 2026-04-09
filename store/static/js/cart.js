document.addEventListener('DOMContentLoaded', () => {

    const forms = document.querySelectorAll('.js-add-to-cart');

    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const button = form.querySelector('[type="submit"]');
            const url = form.action;
            const formData = new FormData(form);

            const originalHTML = button.innerHTML;

            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm text-light"></span>';

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error('Network error');
                }
                
                const data = await response.json();

                if (data.success) {
                    const counter = document.querySelector('.cart-counter');

                    if (counter) {
                        counter.textContent = data.cart_count;

                        if (data.cart_count > 0) {
                            counter.style.display = 'inline-block';
                        } else {
                            counter.style.display = 'none';
                        }

                        counter.classList.add('bump');
                        setTimeout(() => {
                            counter.classList.remove('bump');
                        }, 200);
                    }

                    button.innerHTML = '✓';
                }

            }
            catch (error) {
                console.error('Ошибка:', error);

                button.innerHTML = originalHTML;
                button.disabled = false;

                form.submit();
            }
            finally {
                setTimeout(() => {
                    button.innerHTML = originalHTML;
                    button.disabled = false;
                }, 800);
            }
        });
    });

});
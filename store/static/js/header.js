document.addEventListener('DOMContentLoaded', function () {

    const toggle = document.getElementById('searchToggle');
    const form = document.getElementById('searchForm');

    if (!toggle || !form) return;

    const input = form.querySelector('input');

    // Открытие / закрытие по кнопке
    toggle.addEventListener('click', function (e) {
        e.stopPropagation(); // важно
        form.classList.toggle('active');

        if (form.classList.contains('active')) {
            input.focus();
        }
    });

    // Клик внутри формы НЕ закрывает её
    form.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    // Закрытие при клике вне
    document.addEventListener('click', function () {
        form.classList.remove('active');
    });

});
const cityInput = document.querySelector('[name="city"]');
const cityDropdown = document.getElementById('city-dropdown');

const warehouseInput = document.querySelector('[name="warehouse"]');
const warehouseDropdown = document.getElementById('warehouse-dropdown');

const cityRefInput = document.getElementById('city-ref');

let selectedCityRef = null;


// 🔍 Города
cityInput.addEventListener('input', async () => {
    const query = cityInput.value.trim();

    if (query.length < 2) {
        cityDropdown.innerHTML = '';
        return;
    }

    try {
        const response = await fetch(`/store/api/cities/?q=${query}`);
        const data = await response.json();

        cityDropdown.innerHTML = '';

        data.results.forEach(city => {
            const div = document.createElement('div');
            div.classList.add('dropdown-item');
            div.textContent = city.name;

            div.addEventListener('click', () => {
                cityInput.value = city.name;
                selectedCityRef = city.ref;

                // ✅ сохраняем ref
                cityRefInput.value = city.ref;

                // ✅ очищаем warehouse полностью
                warehouseInput.value = '';
                warehouseDropdown.innerHTML = '';

                cityDropdown.innerHTML = '';
            });

            cityDropdown.appendChild(div);
        });

    } catch (error) {
        console.error('Error loading cities:', error);
    }
});


// 📦 Отделения
warehouseInput.addEventListener('focus', async () => {
    if (!selectedCityRef) return;

    try {
        const response = await fetch(`/store/api/warehouses/?city_ref=${selectedCityRef}`);
        const data = await response.json();

        warehouseDropdown.innerHTML = '';

        data.results.forEach(wh => {
            const div = document.createElement('div');
            div.classList.add('dropdown-item');
            div.textContent = wh.name;

            div.addEventListener('click', () => {
                warehouseInput.value = wh.name;
                warehouseDropdown.innerHTML = '';
            });

            warehouseDropdown.appendChild(div);
        });

    } catch (error) {
        console.error('Error loading warehouses:', error);
    }
});


// ❌ Закрытие dropdown при клике вне
document.addEventListener('click', (e) => {
    if (!e.target.closest('.mb-3')) {
        cityDropdown.innerHTML = '';
        warehouseDropdown.innerHTML = '';
    }
});
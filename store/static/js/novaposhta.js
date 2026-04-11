document.addEventListener('DOMContentLoaded', () => {

    const cityInput = document.querySelector('[name="city"]');
    const cityDropdown = document.getElementById('city-dropdown');

    const warehouseInput = document.querySelector('[name="warehouse"]');
    const warehouseDropdown = document.getElementById('warehouse-dropdown');

    const cityRefInput = document.getElementById('city-ref');

    let selectedCityRef = null;
    let warehousesCache = [];

    let lastCityQuery = 0;

    // ======================
    // debounce
    // ======================
    function debounce(fn, delay = 300) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => fn(...args), delay);
        };
    }

    // ======================
    // render helpers
    // ======================
    function renderList(container, list, onClick) {
        container.innerHTML = '';

        if (!list.length) {
            container.innerHTML = `<div class="dropdown-empty">Нічого не знайдено</div>`;
            return;
        }

        list.forEach(item => {
            const div = document.createElement('div');
            div.classList.add('dropdown-item');
            div.textContent = item.name;

            div.addEventListener('click', () => onClick(item));

            container.appendChild(div);
        });
    }

    function showLoading(container) {
        container.innerHTML = `<div class="dropdown-loading">Завантаження...</div>`;
    }

    // ======================
    // CITY SEARCH
    // ======================
    const handleCityInput = debounce(async () => {
        const query = cityInput.value.trim();

        // 🔥 reset cityRef если пользователь меняет текст
        selectedCityRef = null;
        cityRefInput.value = '';
        warehouseInput.value = '';
        warehousesCache = [];
        warehouseDropdown.innerHTML = '';

        if (query.length < 2) {
            cityDropdown.innerHTML = '';
            return;
        }

        const queryId = ++lastCityQuery;

        showLoading(cityDropdown);

        try {
            const response = await fetch(`/store/api/cities/?q=${query}`);
            const data = await response.json();

            // 🔥 защита от race condition
            if (queryId !== lastCityQuery) return;

            renderList(cityDropdown, data.results, (city) => {
                cityInput.value = city.name;
                selectedCityRef = city.ref;
                cityRefInput.value = city.ref;

                cityDropdown.innerHTML = '';
            });

        } catch (error) {
            cityDropdown.innerHTML = `<div class="dropdown-error">Помилка</div>`;
        }

    }, 300);

    cityInput.addEventListener('input', handleCityInput);

    // ======================
    // WAREHOUSES
    // ======================
    warehouseInput.addEventListener('focus', async () => {
        if (!selectedCityRef) return;

        if (warehousesCache.length) {
            renderList(warehouseDropdown, warehousesCache, selectWarehouse);
            return;
        }

        showLoading(warehouseDropdown);

        try {
            const response = await fetch(`/store/api/warehouses/?city_ref=${selectedCityRef}`);
            const data = await response.json();

            warehousesCache = data.results;

            renderList(warehouseDropdown, warehousesCache, selectWarehouse);

        } catch (error) {
            warehouseDropdown.innerHTML = `<div class="dropdown-error">Помилка</div>`;
        }
    });

    warehouseInput.addEventListener('input', () => {
        const query = warehouseInput.value.toLowerCase().trim();

        const filtered = warehousesCache.filter(wh =>
            wh.name.toLowerCase().includes(query)
        );

        renderList(warehouseDropdown, filtered, selectWarehouse);
    });

    function selectWarehouse(wh) {
        warehouseInput.value = wh.name;
        warehouseDropdown.innerHTML = '';
    }

    // ======================
    // CLOSE DROPDOWNS
    // ======================
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.position-relative')) {
            cityDropdown.innerHTML = '';
            warehouseDropdown.innerHTML = '';
        }
    });

});
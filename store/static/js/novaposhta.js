const cityInput = document.querySelector('[name="city"]');
const cityDropdown = document.getElementById('city-dropdown');

const warehouseInput = document.querySelector('[name="warehouse"]');
const warehouseDropdown = document.getElementById('warehouse-dropdown');

const cityRefInput = document.getElementById('city-ref');

let selectedCityRef = null;
let warehousesCache = [];


function debounce(fn, delay = 300) {
    let timeout;

    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
}


const handleCityInput = debounce(async () => {
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

                cityRefInput.value = city.ref;

                warehouseInput.value = '';
                warehouseDropdown.innerHTML = '';
                warehousesCache = [];

                cityDropdown.innerHTML = '';
            });

            cityDropdown.appendChild(div);
        });

    } catch (error) {
        console.error('Error loading cities:', error);
    }
}, 300);

cityInput.addEventListener('input', handleCityInput);


warehouseInput.addEventListener('focus', async () => {
    if (!selectedCityRef) return;

    if (warehousesCache.length) {
        renderWarehouses(warehousesCache);
        return;
    }

    try {
        const response = await fetch(`/store/api/warehouses/?city_ref=${selectedCityRef}`);
        const data = await response.json();

        warehousesCache = data.results;

        renderWarehouses(warehousesCache);

    } catch (error) {
        console.error('Error loading warehouses:', error);
    }
});


warehouseInput.addEventListener('input', () => {
    const query = warehouseInput.value.toLowerCase().trim();

    const filtered = warehousesCache.filter(wh =>
        wh.name.toLowerCase().includes(query)
    );

    renderWarehouses(filtered);
});


function renderWarehouses(list) {
    warehouseDropdown.innerHTML = '';

    list.forEach(wh => {
        const div = document.createElement('div');
        div.classList.add('dropdown-item');
        div.textContent = wh.name;

        div.addEventListener('click', () => {
            warehouseInput.value = wh.name;
            warehouseDropdown.innerHTML = '';
        });

        warehouseDropdown.appendChild(div);
    });
}


document.addEventListener('click', (e) => {
    if (!e.target.closest('.mb-3')) {
        cityDropdown.innerHTML = '';
        warehouseDropdown.innerHTML = '';
    }
});
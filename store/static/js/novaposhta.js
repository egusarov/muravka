const cityInput = document.querySelector('[name="city"]');
const warehouseInput = document.querySelector('[name="warehouse"]');

let selectedCityRef = null;

// 🔍 Поиск городов
cityInput.addEventListener('input', async () => {
    const query = cityInput.value;

    if (query.length < 2) return;

    const response = await fetch(`/store/api/cities/?q=${query}`);
    const data = await response.json();

    console.log('Cities:', data.results);

    // Пока просто берём первый вариант (упрощение)
    if (data.results.length > 0) {
        selectedCityRef = data.results[0].ref;
    }
});

// 📦 Подгрузка отделений при фокусе
warehouseInput.addEventListener('focus', async () => {
    if (!selectedCityRef) return;

    const response = await fetch(`/store/api/warehouses/?city_ref=${selectedCityRef}`);
    const data = await response.json();

    console.log('Warehouses:', data.results);
});
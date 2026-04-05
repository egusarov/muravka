import requests
from django.conf import settings
from django.core.cache import cache

API_URL = "https://api.novaposhta.ua/v2.0/json/"


def _request(model_name, called_method, method_properties):
    payload = {
        "apiKey": settings.NOVA_POSHTA_API_KEY,
        "modelName": model_name,
        "calledMethod": called_method,
        "methodProperties": method_properties
    }

    response = requests.post(API_URL, json=payload)
    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        return []

    return data.get("data", [])


def get_cities(query):
    cache_key = f"np_cities_{query}"

    cached = cache.get(cache_key)
    if cached:
        return cached

    data = _request(
        model_name="Address",
        called_method="getCities",
        method_properties={
            "FindByString": query,
            "Limit": 10
        }
    )

    result = [
        {
            "name": item["Description"],
            "ref": item["Ref"]
        }
        for item in data
    ]

    cache.set(cache_key, result, 60 * 60 * 24)  # 24 hours
    return result


def get_warehouses(city_ref):
    cache_key = f"np_wh_{city_ref}"

    cached = cache.get(cache_key)
    if cached:
        return cached

    data = _request(
        model_name="Address",
        called_method="getWarehouses",
        method_properties={
            "CityRef": city_ref
        }
    )

    result = [
        {
            "name": item["Description"],
            "ref": item["Ref"]
        }
        for item in data
    ]

    cache.set(cache_key, result, 60 * 60 * 24)  # 24 hours
    return result
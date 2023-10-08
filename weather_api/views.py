import requests
from django.http import JsonResponse
from django.core.cache import cache
from geopy.geocoders import Nominatim
from django.conf import settings


def get_coordinates(city_name):
    try:
        geolocator = Nominatim(user_agent="WeatherGeocoder")
        location = geolocator.geocode(city_name)

        if location:
            latitude = location.latitude
            longitude = location.longitude

            return latitude, longitude
        else:
            return None
    except:
        return None


def get_weather(city_name, cache_timeout=1800):
    data = cache.get(city_name)

    if data is None:
        coord = get_coordinates(city_name)
        if coord:
            lat, lon = coord
            url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
            headers = {
                "X-Yandex-API-Key": settings.API_YANDEX_KEY,
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                cache.set(city_name, data, cache_timeout)
            else:
                return None
        else:
            return None
    return data


def weather_view(request):
    city_name = request.GET.get("city", "")

    if not city_name:
        return JsonResponse({"error": "Параметр 'city' не указан в запросе."}, status=400)

    weather_data = get_weather(city_name)

    if weather_data:
        temperature = weather_data["fact"]["temp"]
        pressure_mm = weather_data["fact"]["pressure_mm"]
        wind_speed = weather_data["fact"]["wind_speed"]
        return JsonResponse({
            "city": city_name,
            "temperature": temperature,
            "pressure_mm": pressure_mm,
            "wind_speed": wind_speed
        }, status=200)
    else:
        return JsonResponse({"error": "Не удалось получить данные о погоде."}, status=500)

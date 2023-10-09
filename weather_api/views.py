import requests
from django.http import JsonResponse
from django.core.cache import cache
from geopy.geocoders import Nominatim
from django.conf import settings
import geopy.exc


def get_coordinates(city_name):
    try:
        geolocator = Nominatim(user_agent="WeatherGeocoder")
        location = geolocator.geocode(city_name)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
    except geopy.exc.GeocoderTimedOut as e:
        print(e)

    return None, None


def get_weather(city_name, cache_timeout=1800):
    data = cache.get(city_name)

    if data is None:
        lat, lon = get_coordinates(city_name)

        if lat is not None and lon is not None:
            url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
            headers = {
                "X-Yandex-API-Key": settings.API_YANDEX_KEY,
            }

            try:
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    cache.set(city_name, data, cache_timeout)
            except requests.RequestException as e:
                print(e)

    return data


def weather_view(request):
    city_name = request.GET.get("city", "")

    if not city_name:
        return JsonResponse({"error_code": "400", "error_message": "Параметр 'city' не указан в запросе."}, status=400)

    weather_data = get_weather(city_name)

    if weather_data:
        fact = weather_data.get("fact", {})

        temperature = fact.get("temp")
        pressure_mm = fact.get("pressure_mm")
        wind_speed = fact.get("wind_speed")

        if all((temperature, pressure_mm, wind_speed)):
            return JsonResponse({
                "city": city_name,
                "temperature": temperature,
                "pressure_mm": pressure_mm,
                "wind_speed": wind_speed
            }, status=200)

    return JsonResponse({"error_code": "500", "error_message": "Не удалось получить данные о погоде."}, status=500)

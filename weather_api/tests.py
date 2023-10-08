from django.test import TestCase, Client


class WeatherViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_weather_success(self):
        response = self.client.get(f"/weather?city=Kaliningrad")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        # Проверьте, что данные о погоде верны
        data = response.json()
        self.assertEqual(data["city"], "Kaliningrad")
        self.assertIsNotNone(data["temperature"])
        self.assertIsNotNone(data["pressure_mm"])
        self.assertIsNotNone(data["wind_speed"])

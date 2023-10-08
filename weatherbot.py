import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = '6467616964:AAGCf5AFTSfDPgIvnWMqSBk0wNp6NxBUG5k'
API_URL = 'http://0.0.0.0:8000/weather'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Узнать погоду")
    keyboard.add(button)

    await message.answer("Привет! Я бот для узнавания погоды. Нажми 'Узнать погоду', чтобы начать.",
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text.lower() == "узнать погоду")
async def get_weather(message: types.Message):
    await message.answer("Введите название города для получения погоды:")


@dp.message_handler(lambda message: message.text and not message.text.lower() == "узнать погоду")
async def process_city(message: types.Message):
    city_name = message.text

    try:
        response = requests.get(f"{API_URL}?city={city_name}")
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data.get("temperature", "недоступно")
            pressure_mm = weather_data.get("pressure_mm", "недоступно")
            wind_speed = weather_data.get("wind_speed", "недоступно")

            weather_message = (
                f"Погода в городе {city_name}:\n"
                f"Температура: {temperature}°C\n"
                f"Атмосферное давление: {pressure_mm} мм рт.ст.\n"
                f"Скорость ветра: {wind_speed} м/с"
            )

            await message.answer(weather_message)
        else:
            await message.answer("Не удалось получить данные о погоде.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# Проект Weather API

![GitHub](https://img.shields.io/github/license/Lespir/weather_project)

Проект WeatherBot представляет собой Django веб-приложение и Telegram бота для получения текущей погоды в различных городах.

## Описание проекта

Этот проект включает в себя веб-приложение, созданное с использованием Django, которое позволяет пользователю получать информацию о текущей погоде в выбранном городе. При первом запросе для каждого города, проект получает данные о погоде от Yandex, а затем кеширует их на некоторое время для ускорения последующих запросов.

Также в проекте присутствует Telegram бот, реализованный с помощью библиотеки Aiogram. Бот позволяет пользователям узнавать прогноз погоды на сегодня для заданного города.

## Как использовать проект

Чтобы использовать этот проект, выполните следующие шаги:

1. **Клонируйте репозиторий**:

   ```bash
   git clone https://github.com/Lespir/weather_project.git
   ```
   
2. **Создайте вертуальное окружение проекта**:

   Перейдите в корневую директорию проекта, создайте вертуальное окружение и запустите его:

   ```bash
   сd weather_project
   python -m venv venv
   source venv/bi/activate
   ```
   
2. **Установите зависимости**:

   Установите зависимости, указанные в файле `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Создайте кеш-таблицу**:

   Запустите следующую команду для создания кеш-таблицы в базе данных:

   ```bash
   python manage.py createcachetable
   ```

4. **Запустите Django приложение**:

   Запустите Django приложение с помощью следующей команды:

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

   Приложение будет доступно по адресу `http://localhost:8000/`.
   
   Вы можете запустить автоматические тесты для приложения weather_api с помощью следующей команды:

   ```bash
   python manage.py test weather_api
   ```

6. **Запустите Telegram бота**:

   Запустите Telegram бота, который находится в файле `weatherbot.py`, отдельно от Django приложения.

   ```bash
   python weatherbot.py
   ```

   Бот будет доступен через Telegram мессенджер [@WeatherYndxBot](https://t.me/WeatherYndxBot)

Для получения погоды по API Django сервиса необходимо отправить GET-запрос `http://0.0.0.0:8000/weather?city=<city_name>`, где <city_name> - это название города,
в ответе будет содержаться информация о текущую температуру в этом городе в градусах Цельсия, атмосферное давление (мм рт.ст) и скорость ветра (м/с).

## Комментарии по реализации

Docker может быть отличным инструментом для упрощения развёртывания и одновременного запуска Django-проекта и Telegram бота в единой среде. Это можно реализовать с использованием Docker Compose. Однако я посчитал это излишним усложнение для тестового проекта. Реализация данного решения могла бы привезти к недопониманию со стороны проверющего и неоправданно усложнило бы процесс проверки.

## Лицензия

Проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

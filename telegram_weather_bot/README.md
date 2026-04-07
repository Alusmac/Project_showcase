# 🌤 Telegram Weather Bot

Telegram бот, який дозволяє дізнатися актуальну погоду. 
Бот працює через Telegram API та отримує дані через зовнішнє Weather API (OpenWeatherMap).
Бот працює асинхронно:

На відміну від синхронних ботів, цей проект:
* **Не блокується:** Поки бот чекає відповіді від Weather API для одного міста,
* він може приймати команди від інших користувачів.
---

## Як запустити проект локально

1. **Клонувати репозиторій:**
   ```bash
   git clone [https://github.com/Alusmac/Project_showcase.git](https://github.com/Alusmac/Project_showcase.git)
   cd Project_showcase/telegram_bot_weather
2. **Налаштувати віртуальне середовище:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # для macOS/Linux
    .venv\Scripts\activate     # для Windows
3. **Встановити залежності:**
    ```bash
   pip install -r requirements.txt
4. **Створити файл .env з токенами:**
    ```bash
   TELEGRAM_TOKEN=secret_key
   WEATHER_API_KEY=secret_key
5. **Запустити бот:**
     ```bash
    python telegram_bot.py
   
**Використані API:**
1. Telegram Bot API — для взаємодії з користувачем та обробки команд.

2. Weather API (OpenWeatherMap) — для отримання точних метеорологічних даних.

**Приклад роботи програми**

Користувач: /start

Бот: Привіт! Я бот для перевірки погоди. Введи /weather <місто>, щоб отримати прогноз.

Користувач: /weather Kyiv

Бот: > Погода у Києві:

 Температура: 15°C
️ Опис: Ясно

Користувач: /help

Бот: Список команд: /start, /help, /weather <місто>

**Посилання на бота**

Ви можете протестувати бота за посиланням: t.me/av_weather_bot
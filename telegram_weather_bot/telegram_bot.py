import os
import logging
import aiohttp
import ssl
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from weather_api import fetch_weather
import asyncio

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

user_states = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued
    """
    await update.message.reply_text(
        "Привіт! 👋 Я бот погоди.\nНапиши /help щоб побачити команди."
    )
    logging.info(f"User {update.effective_user.id} started bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued
    """
    await update.message.reply_text(
        "/start - запуск бота\n"
        "/help - список команд\n"
        "/weather - дізнатися погоду"
    )


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /weather is issued
    """
    user_states[update.effective_user.id] = "waiting_city"
    await update.message.reply_text("Вкажіть місто:")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user messages in telegram bot
    """
    user_id = update.effective_user.id
    text = update.message.text

    if user_states.get(user_id) == "waiting_city":
        cities = [c.strip() for c in text.split(",") if c.strip()]

        try:
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            connector = aiohttp.TCPConnector(ssl=ssl_context)

            async with aiohttp.ClientSession(connector=connector) as session:

                tasks = [fetch_weather(session, city) for city in cities]
                results = await asyncio.gather(*tasks)

            responses = []

            for city, data in zip(cities, results):
                if "error" in data:
                    responses.append(f"❌ {city}: {data['error']}")
                    logging.error(f"Error for {city}: {data['error']}")
                else:
                    temp = data["main"]["temp"]
                    description = data["weather"][0]["description"]
                    responses.append(f"🌤 {city}: {temp}°C, {description}")

                    logging.info(f"Weather fetched for {city}")

            await update.message.reply_text("\n".join(responses))

        except Exception as e:
            logging.error(f"[CRITICAL ERROR] {str(e)}")
            await update.message.reply_text("⚠️ Помилка при отриманні даних")

        finally:
            user_states[user_id] = None


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("weather", weather))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    logging.info("Bot started")

    app.run_polling()


if __name__ == "__main__":
    main()

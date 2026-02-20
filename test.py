import asyncio
import aiohttp
from weather_api import fetch_weather, fetch_forecast
from display import show_weather, show_forecast


async def main():
    cities_input = input("Введіть назви міст через кому: ")
    cities = [city.strip() for city in cities_input.split(",") if city.strip()]

    async with aiohttp.ClientSession() as session:
        for city in cities:
            print("\n=== Поточна погода ===")
            current_data = await fetch_weather(session, city)
            show_weather(current_data)

            print("\n=== Прогноз на 5 днів ===")
            forecast_data = await fetch_forecast(session, city)
            show_forecast(forecast_data)


if __name__ == "__main__":
    asyncio.run(main())

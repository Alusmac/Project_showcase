import asyncio
import aiohttp
import ssl
from weather_api import fetch_weather, fetch_forecast
from display import show_weather, show_forecast


async def main():
    """Main program entry: asks user for city names and displays weather info
    """
    cities_input = input("Enter the names of cities in English, separating them with commas: ")
    cities = [city.strip() for city in cities_input.split(",") if city.strip()]

    # ┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅
    # SSL fix for MacOS!!!
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    # ┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        for city in cities:
            print("\n┅┅┅┅┅ Current weather ┅┅┅┅┅")
            current_data = await fetch_weather(session, city)
            show_weather(current_data)

            print("\n┅┅┅┅┅ 5-Day Forecast ┅┅┅┅┅")
            forecast_data = await fetch_forecast(session, city)
            show_forecast(forecast_data)


if __name__ == "__main__":
    asyncio.run(main())

import aiohttp
from typing import Dict

API_KEY = "c46d0f307cd4846b3e7e0ca1a90d6b05"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


async def fetch_weather(session: aiohttp.ClientSession, city: str) -> Dict:
    """Gets current weather data for a given city
    """
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "en"}
    try:
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 401:
                return {"error": "Invalid or inactive API key"}
            if response.status != 200:
                return {"error": f"City '{city}' not found"}
            return await response.json()
    except aiohttp.ClientConnectionError:
        return {"error": f"[CONNECTION ERROR] Cannot connect to server for '{city}'"}
    except Exception as e:
        return {"error": str(e)}


async def fetch_forecast(session: aiohttp.ClientSession, city: str) -> Dict:
    """ Gets current weather data for 5 days for a given city
    """
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "en"}
    try:
        async with session.get(FORECAST_URL, params=params) as response:
            if response.status == 401:
                return {"error": "Invalid or inactive API key"}
            if response.status != 200:
                return {"error": f"City '{city}' not found"}
            return await response.json()
    except aiohttp.ClientConnectionError:
        return {"error": f"[CONNECTION ERROR] Cannot connect to server for '{city}'"}
    except Exception as e:
        return {"error": str(e)}

from colorama import Fore, Style, init

init(autoreset=True)

WEATHER_ICONS = {
    "clear": "🌞",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️"
}


def get_icon(description: str) -> str:
    """ Returns a weather icon based on a description
    """
    desc = description.lower()
    for key, icon in WEATHER_ICONS.items():
        if key in desc:
            return icon
    return "🌡️"


def show_weather(data: dict) -> None:
    """ Display current weather with color and icon
    """
    if "error" in data:
        print(Fore.RED + data["error"])
        return

    name = data.get("name")
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    icon = get_icon(weather)

    print(Fore.BLUE + Style.BRIGHT + f"\nWeather in {name}:")
    print(Fore.GREEN + f"{icon} {weather.capitalize()}")
    print(Fore.MAGENTA + f"Temperature: {temp}°C")
    print(Fore.CYAN + f"Humidity: {humidity}%")


def show_forecast(forecast_data: dict) -> None:
    """Display 5-day weather forecast with color and icons
    """
    if "error" in forecast_data:
        print(Fore.RED + forecast_data["error"])
        return

    city_name = forecast_data["city"]["name"]
    print(Fore.BLUE + Style.BRIGHT + f"\n5-day forecast for {city_name}:")

    daily = {}
    for item in forecast_data["list"]:
        date = item["dt_txt"].split(" ")[0]
        temp = item["main"]["temp"]
        weather = item["weather"][0]["description"]
        daily.setdefault(date, []).append((temp, weather))

    for date, values in daily.items():
        avg_temp = sum([t for t, _ in values]) / len(values)
        weather_modes = [w for _, w in values]
        most_common_weather = max(set(weather_modes), key=weather_modes.count)
        icon = get_icon(most_common_weather)
        print(Fore.MAGENTA + f"{date}: {icon} {most_common_weather.capitalize()}, Temperature: {avg_temp:.1f}°C")

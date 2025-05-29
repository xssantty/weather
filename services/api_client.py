import aiohttp
import asyncio
from config.settings import settings

class WeatherAPI:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    CACHE = {}

    async def get_weather(self, city: str, lang="ru", force_refresh=False):
        key = (city.lower(), lang)
        if key in self.CACHE and not force_refresh:
            return self.CACHE[key]

        params = {
            "q": city,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric",
            "lang": lang  
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.BASE_URL, params=params, timeout=5) as resp:
                    if resp.status != 200:
                        raise Exception("Город не найден")
                    data = await resp.json()

                    result = {
                        "city": data["name"],
                        "temp": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"],
                        "description": data["weather"][0]["description"]
                    }

                    self.CACHE[key] = result
                    return result

            except asyncio.TimeoutError:
                raise Exception("⏳ Превышено время ожидания.")
            except Exception as e:
                raise Exception("❌ Ошибка получения данных о погоде.")

def format_weather(data, lang="ru"):
    if lang == "en":
        return (
            f"🌍 City: {data['city']}\n"
            f"🌡 Temperature: {data['temp']}°C\n"
            f"💧 Humidity: {data['humidity']}%\n"
            f"🌬 Wind speed: {data['wind_speed']} m/s\n"
            f"☁️ Weather: {data['description'].capitalize()}"
        )
    else:
        return (
            f"🌍 Город: {data['city']}\n"
            f"🌡 Температура: {data['temp']}°C\n"
            f"💧 Влажность: {data['humidity']}%\n"
            f"🌬 Ветер: {data['wind_speed']} м/с\n"
            f"☁️ Погода: {data['description'].capitalize()}"
        )

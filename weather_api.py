import aiohttp
import asyncio
import logging

async def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 65.754927,  # Сколтех
        "longitude": 37.621781,
        "current": ["temperature_2m", "precipitation", "surface_pressure", "wind_speed_10m", "wind_direction_10m"],
        "daily": "precipitation_sum",
        "timezone": "Europe/Moscow",
    }

    direction = ("С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ")

    for _ in range(3):  # Попытки повторного запроса
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        weather = data["current"]
                        # Преобразование скорости ветра км/ч в м/с
                        direction_i = int((weather["wind_direction_10m"] + 22.5) // 45)
                        if direction_i == 8:
                            direction_i = 0
                        return {
                            "temperature": weather["temperature_2m"],
                            "wind_speed": weather["wind_speed_10m"] * 1000 // 3600,
                            "wind_direction": direction[direction_i],
                            "pressure": weather["surface_pressure"],

                            "precipitation_sum": sum(data["daily"]["precipitation_sum"]),
                            # Преобразование значения осадков
                            "precipitation_type": weather["precipitation"]
                            if weather["precipitation"] or weather["precipitation"] not in [0.0, '0.0']
                            else "Без осадков"
                        }
                    else:
                        logging.warning(f"Ошибка HTTP {response.status}: {response.reason}")
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка соединения с API: {e}")
        await asyncio.sleep(5)  # Задержка перед повторной попыткой
    return None

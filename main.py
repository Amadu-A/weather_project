import asyncio
from database import async_session, init_db
from weather_api import fetch_weather
from models import WeatherData
from export import export_to_excel
import logging

logging.basicConfig(level=logging.INFO)

async def save_weather_data(session, data):
    try:
        weather = WeatherData(
            temperature=data["temperature"],
            wind_speed=data["wind_speed"],
            wind_direction=data["wind_direction"],
            pressure=data["pressure"],
            precipitation_type=data["precipitation_type"],
            precipitation_sum=data["precipitation_sum"]
        )
        session.add(weather)
        await session.commit()
        logging.info("Данные о погоде успешно сохранены в базу данных.")
    except Exception as e:
        await session.rollback()
        logging.error(f"Ошибка при сохранении данных в БД: {e}")

async def weather_monitor():
    await init_db()
    while True:
        async with async_session() as session:
            weather_data = await fetch_weather()
            if weather_data:
                await save_weather_data(session, weather_data)
        await asyncio.sleep(180)  # каждые 3 минуты

async def get_user_input():
    loop = asyncio.get_event_loop()
    while True:
        command = await loop.run_in_executor(None, input, "Введите 'export' для экспорта данных: ")
        if command.lower() == "export":
            async with async_session() as session:
                await export_to_excel(session)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(weather_monitor())
    loop.create_task(get_user_input())
    loop.run_forever()

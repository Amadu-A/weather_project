import asyncio
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import WeatherData


async def export_to_excel(session: AsyncSession):
    # Функция для синхронного выполнения экспорта
    def sync_export(data):
        df = pd.DataFrame(data)
        df.to_excel("weather_data.xlsx", index=False)

    # Запрос к базе данных для получения 10 последних записей
    result = await session.execute(
        select(WeatherData).order_by(WeatherData.timestamp.desc()).limit(10)
    )
    records = result.scalars().all()
    print(records)
    # direction[(int(r.wind_direction) + 22,5) // 45]
    # Преобразование данных в формат, пригодный для экспорта
    data = [
        {
            "Temperature": r.temperature,
            "Wind Speed": r.wind_speed,
            "Wind Direction": r.wind_direction,
            "Pressure": r.pressure,
            "Precipitation Type": r.precipitation_type,
            "Precipitation Amount": r.precipitation_sum,
            "Timestamp": r.timestamp
        }
        for r in records
    ]

    # Выполнение экспорта в отдельном потоке
    await asyncio.get_event_loop().run_in_executor(None, sync_export, data)

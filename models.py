from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_direction = Column(String, nullable=False)
    pressure = Column(Float, nullable=False)
    precipitation_type = Column(String, nullable=True)
    precipitation_sum = Column(Float, nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)

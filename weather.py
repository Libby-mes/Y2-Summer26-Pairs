import asyncio
import python_weather

async def get_weather(city):
    async with python_weather.Client() as client:
        weather = await client.get(city)

        return f"The current weather in {city} is {weather.temperature}°C with {weather.description}."

def get_weather_sync(city):
    return asyncio.run(get_weather(city))
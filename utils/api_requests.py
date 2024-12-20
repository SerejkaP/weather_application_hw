from datetime import datetime

import aiohttp

URL = "https://api.openweathermap.org/"

async def get_data_async(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def get_weather_async(city:str, api_key:str):
    # Вернет локализованное название города и температуру
    city_info_url = URL+f"geo/1.0/direct?q={city}&appid={api_key}"
    city_info = await get_data_async(city_info_url)
    if 'cod' in city_info and city_info['cod'] == 401:
        return 401, None, None, None
    lat, lon = city_info[0]['lat'], city_info[0]['lon']
    weather_url = URL+f"data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    weather = await get_data_async(weather_url)
    return 200, city_info[0]['local_names']['ru'], datetime.fromtimestamp(weather['sys']['sunrise']), float(weather['main']['temp'])
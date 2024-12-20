from typing import Optional

import pandas as pd
import streamlit as st
import asyncio
from utils.api_requests import get_weather_async
from utils.data_processing import process_data, process_season_data
from utils.season_helper import get_season
from utils.visualization import plot_time_series

API_KEY:Optional[str] = None
uploaded_data:Optional[pd.DataFrame] = None
city:Optional[str] = None

async def process_main_page():
    show_main_page()
    await process_side_bar_inputs()


def show_main_page():

    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Weather App",
    )

    st.write(
        """
        # Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API
        """
    )

def show_table(df:pd.DataFrame):
    st.write("Ваши данные:")
    st.table(df.sample(10))

async def show_city_info(data:pd.DataFrame, city_name:str):
    st.write(
        f"""
        ## {city_name}  
        ### Анализ исторических данных
        """
    )
    # График временных рядов для температуры
    fig = plot_time_series(data[data['city'] == city_name], city_name)
    st.pyplot(fig)

    # Получение средней температуры, отклонения и минимальной и максимальной температуры по сезонам
    info_data = process_season_data(data[data['city'] == city_name]).drop('city', axis=1)
    st.table(info_data)

    if API_KEY is not None and len(API_KEY) > 0:
        code, locale_city_name, date_time, temperature = await get_weather_async(city_name, API_KEY)
        if code == 401:
            st.write("Неверный ключ OpenWeatherMap. Для более подробной информации: https://openweathermap.org/faq#error401")
        else:
            st.write(f"### Температура в городе {locale_city_name}: {temperature} градусов ({date_time})")
            season = get_season(date_time)
            historical_season_data = info_data[info_data['season'] == season]
            lower_bound = historical_season_data['average'].iloc[0] - 2*historical_season_data['std'].iloc[0]
            upper_bound = historical_season_data['average'].iloc[0] + 2*historical_season_data['std'].iloc[0]

            if temperature < lower_bound:
                st.write("Аномально низкая температура")
                if temperature < historical_season_data['min'].iloc[0]:
                    st.write("Новый  исторический минимум!")
            elif temperature > upper_bound:
                st.write("Аномально высока температура")
                if temperature > historical_season_data['max'].iloc[0]:
                    st.write("Новый  исторический максимум!")
            else:
                st.write("Температура соответствует историческим данным")


async def process_side_bar_inputs():
    global API_KEY, uploaded_data, city
    st.sidebar.header('Меню')
    API_KEY = st.sidebar.text_input("Ключ OpenWeatherMap", type="password")

    csv_file = st.sidebar.file_uploader("Загрузить csv-файл с данными")
    data = None
    if csv_file is not None and csv_file.name[-4:] == ".csv":
        data = pd.read_csv(csv_file)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        uploaded_data = process_data(data.copy())
        show_cities = True
    else:
        uploaded_data = None
        show_cities = False
        city = None

    if show_cities:
        city = st.sidebar.selectbox("Выберите город", options=[None, *uploaded_data['city'].unique()])
        if city is None:
            show_table(data)
        else:
            await show_city_info(uploaded_data, city)
    else:
        st.write(
            """
            * **Для работы с приложением необходимо загрузить csv-файл, содержащий:**
                - `city`: Название города.
                - `timestamp`: Дата (с шагом в 1 день).
                - `temperature`: Среднесуточная температура (в °C).
                - `season`: Сезон года (зима, весна, лето, осень).

            * Для работы с текущей температурой следует указать ключ OpenWeatherMap API
            """
        )

if __name__ == "__main__":
    asyncio.run(process_main_page())
import matplotlib.pyplot as plt
import pandas as pd


def plot_time_series(data: pd.DataFrame, city: str):
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(data['timestamp'], data['temperature'], label='Температура')
    ax.plot(data['timestamp'], data['rolling_mean'], label='Скользящее среднее с окном в 30 дней', color='orange')
    ax.scatter(data[data['anomaly_temperature'] == True]['timestamp'], data[data['anomaly_temperature'] == True]['temperature'], s=3, c='red', label='Аномалии')
    ax.set_title(f'Температура по времени для {city}', fontsize=14)
    ax.set_xlabel('Дата', fontsize=12)
    ax.set_ylabel('Температура', fontsize=12)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    return fig
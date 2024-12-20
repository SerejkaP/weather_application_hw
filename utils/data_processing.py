import pandas as pd

def process_data(data: pd.DataFrame):
    data['rolling_mean'] = data.groupby('city')['temperature'].transform(lambda x: x.rolling(window=30).mean())
    data['rolling_std'] = data.groupby('city')['temperature'].transform(lambda x: x.rolling(window=30).std())
    data['lower_bound'] = data['rolling_mean'] - 2 * data['rolling_std']
    data['upper_bound'] = data['rolling_mean'] + 2 * data['rolling_std']
    data['anomaly_temperature'] = (data['temperature'] < data['lower_bound']) | (data['temperature'] > data['upper_bound'])
    return data

def process_season_data(data:pd.DataFrame):
    return data.groupby(['city', 'season'])['temperature'].agg(average='mean', std='std', min='min', max='max').reset_index()
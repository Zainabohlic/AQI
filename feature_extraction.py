import hopsworks
import pandas as pd

# Login to the project with your API key
project = hopsworks.login(api_key_value="Jc6KapH8rIxyGs3y.OHbQCJktzLQVPtSRiVPUiM5ZRWFGokVXgbJX8zgcKRKvAlWlhnLLE4ky8hFcXiuj")

# Get the feature store
feature_store = project.get_feature_store()

# Fetch the feature group
aqi_fg = feature_store.get_feature_group(name="aqi_data", version=1)

# Load your CSV file into a pandas DataFrame
df = pd.read_csv("/Users/zainabaslam/Local Docs/10Pearls/processed_aqi_weather_data.csv")

# Preprocessing steps...
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df['weekday'] = df['date'].dt.weekday

# Lag features
df['aqi_lag_1'] = df['aqi'].shift(1)
df['aqi_lag_24'] = df['aqi'].shift(24)
df['aqi_lag_168'] = df['aqi'].shift(168)

# Handle missing values
df = df.dropna(subset=['pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co', 'hour', 'day', 'month', 'year', 'weekday', 'aqi_change_rate', 'aqi_lag_1', 'aqi_lag_24', 'aqi_lag_168'])

# Save the updated data back to the feature store (or update the feature group if needed)
# Note: Here you would interact with the feature group API to store new data.

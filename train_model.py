import hopsworks
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Login to the project with your API key
project = hopsworks.login(api_key_value="Jc6KapH8rIxyGs3y.OHbQCJktzLQVPtSRiVPUiM5ZRWFGokVXgbJX8zgcKRKvAlWlhnLLE4ky8hFcXiuj")

# Get the feature store and feature group
feature_store = project.get_feature_store()
aqi_fg = feature_store.get_feature_group(name="aqi_data", version=1)

# Fetch data from feature group
df = aqi_fg.read()

# Preprocessing (as in your original code)
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df['weekday'] = df['date'].dt.weekday

df['aqi_lag_1'] = df['aqi'].shift(1)
df['aqi_lag_24'] = df['aqi'].shift(24)
df['aqi_lag_168'] = df['aqi'].shift(168)

# Handling missing values
df = df.dropna(subset=['pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co', 'hour', 'day', 'month', 'year', 'weekday', 'aqi_change_rate', 'aqi_lag_1', 'aqi_lag_24', 'aqi_lag_168'])

# Feature selection and scaling
features = ['pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co', 'hour', 'day', 'month', 'year', 'weekday', 'aqi_change_rate', 'aqi_lag_1', 'aqi_lag_24', 'aqi_lag_168']
X = df[features]
y = df['aqi']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")

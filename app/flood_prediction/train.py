import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data/processed/arrah_water_levels.csv"
MODEL_DIR = PROJECT_ROOT / "data/model_evaluation/trained_model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODEL_DIR / "river_level_model.joblib"

print("Loading prepared river data...")

df = pd.read_csv(DATA_FILE, parse_dates=["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

# Previous observed levels are the input features.
for lag in [1, 2, 3, 6, 12, 24]:
    df[f"lag_{lag}"] = df["water_level"].shift(lag)

df["hour"] = df["timestamp"].dt.hour
df["month"] = df["timestamp"].dt.month

df = df.dropna().reset_index(drop=True)

features = [
    "lag_1", "lag_2", "lag_3",
    "lag_6", "lag_12", "lag_24",
    "hour", "month"
]

X = df[features]
y = df["water_level"]

# Chronological split: earlier observations train, later observations test.
split = int(len(df) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

print("Training observations:", len(X_train))
print("Testing observations:", len(X_test))

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=12,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Random Forest model...")
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

# Persistence baseline: predict the next level equals the last observed level.
baseline = X_test["lag_1"]

baseline_mae = mean_absolute_error(y_test, baseline)

joblib.dump(
    {
        "model": model,
        "features": features,
        "station": "Arrah Chhapra Bridge"
    },
    MODEL_FILE
)

print("\nMODEL EVALUATION")
print("-------------------------")
print(f"Model MAE: {mae:.4f} m")
print(f"Model RMSE: {rmse:.4f} m")
print(f"Model R2: {r2:.4f}")
print(f"Baseline MAE: {baseline_mae:.4f} m")

print("\nModel saved to:", MODEL_FILE)
import pandas as pd
import joblib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    ROOT / "data/model_evaluation/trained_model/"
    "river_level_model.joblib"
)

DATA_FILE = ROOT / "data/processed/arrah_water_levels.csv"

bundle = joblib.load(MODEL_FILE)
model = bundle["model"]
features = bundle["features"]

df = pd.read_csv(DATA_FILE, parse_dates=["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

row = df.iloc[-1]

values = {}

for lag in [1, 2, 3, 6, 12, 24]:
    values[f"lag_{lag}"] = df["water_level"].iloc[-lag]

values["hour"] = row["timestamp"].hour
values["month"] = row["timestamp"].month

input_data = pd.DataFrame([values])[features]

prediction = model.predict(input_data)[0]

print("STATION: Arrah Chhapra Bridge")
print("Last recorded time:", row["timestamp"])
print("Last recorded water level:", row["water_level"], "m")
print("Predicted next observation:", round(prediction, 3), "m")
print("Prediction type: Experimental river-level forecast")
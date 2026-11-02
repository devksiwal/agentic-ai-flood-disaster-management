import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT / "data/raw/bihar/"
    "rwl_tel_hr_bihar_999_2021_2025.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data/processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "arrah_water_levels.csv"

print("Loading Arrah Chhapra Bridge observations...")

parts = []

for chunk in pd.read_csv(INPUT_FILE, chunksize=100000):
    selected = chunk[
        chunk["Station"].astype(str).str.strip()
        == "Arrah Chhapra Bridge"
    ]

    if not selected.empty:
        parts.append(selected[[
            "Data Acquisition Time",
            "River Water Level Telemetry Hourly (meter)"
        ]])

df = pd.concat(parts, ignore_index=True)

df["timestamp"] = pd.to_datetime(
    df["Data Acquisition Time"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

df["water_level"] = pd.to_numeric(
    df["River Water Level Telemetry Hourly (meter)"],
    errors="coerce"
)

df = df.dropna(subset=["timestamp", "water_level"])

# Flag extreme values for exclusion from this prototype.
# This is a statistical screening rule, not a verified physical limit.
df["is_extreme"] = df["water_level"] > 100

extreme_count = int(df["is_extreme"].sum())

df = df[~df["is_extreme"]]

# Combine duplicate timestamps using the median.
df = (
    df.groupby("timestamp", as_index=False)["water_level"]
    .median()
    .sort_values("timestamp")
)

df.to_csv(OUTPUT_FILE, index=False)

print("\nDATA PREPARATION COMPLETE")
print("Extreme readings excluded:", extreme_count)
print("Unique timestamps:", len(df))
print("First timestamp:", df["timestamp"].min())
print("Last timestamp:", df["timestamp"].max())
print("Output:", OUTPUT_FILE)

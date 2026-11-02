import pandas as pd

FILE = "data/raw/bihar/rwl_tel_hr_bihar_999_2021_2025.csv"
STATION = "Arrah Chhapra Bridge"

data = []

for chunk in pd.read_csv(FILE, chunksize=100000):
    selected = chunk[chunk["Station"] == STATION]

    if not selected.empty:
        data.append(selected[[
            "Data Acquisition Time",
            "River Water Level Telemetry Hourly (meter)"
        ]])

df = pd.concat(data, ignore_index=True)

df["time"] = pd.to_datetime(
    df["Data Acquisition Time"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

df["level"] = pd.to_numeric(
    df["River Water Level Telemetry Hourly (meter)"],
    errors="coerce"
)

df = df.dropna(subset=["time", "level"])

print("Valid records:", len(df))
print("Date range:", df["time"].min(), "to", df["time"].max())
print("Unique timestamps:", df["time"].nunique())
print("Duplicate timestamps:", df["time"].duplicated().sum())

print("\nPercentiles:")
print(df["level"].quantile([0, .01, .05, .25, .50, .75, .95, .99, 1]))

print("\nReadings above 100:", (df["level"] > 100).sum())
print("Readings above 200:", (df["level"] > 200).sum())

print("\nMost frequent readings:")
print(df["level"].value_counts().head(10))
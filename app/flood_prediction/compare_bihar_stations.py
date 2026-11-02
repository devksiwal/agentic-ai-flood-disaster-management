import pandas as pd

FILE_PATH = "data/raw/bihar/rwl_tel_hr_bihar_999_2021_2025.csv"

station_stats = []

for chunk in pd.read_csv(
    FILE_PATH,
    usecols=[
        "Station",
        "District",
        "River Water Level Telemetry Hourly (meter)"
    ],
    chunksize=100000
):

    chunk["WaterLevel"] = pd.to_numeric(
        chunk["River Water Level Telemetry Hourly (meter)"],
        errors="coerce"
    )

    grouped = chunk.groupby("Station")

    for station, group in grouped:

        values = group["WaterLevel"].dropna()

        if values.empty:
            continue

        station_stats.append({
            "Station": station,
            "District": group["District"].iloc[0],
            "Records": len(group),
            "Valid_Readings": len(values),
            "Unique_Values": values.nunique(),
            "Most_Common_Value": values.mode().iloc[0],
            "Most_Common_Count": values.value_counts().iloc[0]
        })

df = pd.DataFrame(station_stats)

summary = (
    df.groupby(["Station", "District"], as_index=False)
    .agg({
        "Records": "sum",
        "Valid_Readings": "sum",
        "Unique_Values": "sum",
        "Most_Common_Count": "sum"
    })
)

summary["Repeated_Value_Percent"] = (
    summary["Most_Common_Count"]
    / summary["Valid_Readings"]
    * 100
)

print("\nBIHAR STATION DATA QUALITY COMPARISON\n")

print(
    summary.sort_values(
        "Repeated_Value_Percent"
    ).to_string(index=False)
)

summary.to_csv(
    "data/processed/bihar_station_comparison.csv",
    index=False
)

print("\nReport saved to data/processed/bihar_station_comparison.csv")
import pandas as pd

file_path = "data/raw/bihar/rwl_tel_hr_bihar_999_2021_2025.csv"

columns = [
    "Station",
    "District",
    "River",
    "Basin",
    "Latitude",
    "Longitude"
]

stations = set()

print("Inspecting Bihar river and basin information...")

for chunk in pd.read_csv(
    file_path,
    usecols=columns,
    chunksize=100000
):
    valid = chunk[
        (chunk["River"].notna()) &
        (chunk["River"].astype(str).str.strip() != "-") &
        (chunk["Basin"].notna()) &
        (chunk["Basin"].astype(str).str.strip() != "-")
    ]

    for row in valid[columns].drop_duplicates().itertuples(
        index=False, name=None
    ):
        stations.add(row)

print("\nSTATIONS WITH IDENTIFIED RIVERS AND BASINS:")

for station in sorted(stations):
    print(station)

print("\nTotal identified station combinations:", len(stations))
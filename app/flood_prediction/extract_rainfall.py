import pdfplumber
import re
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PDF_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "imd"
    / "DISTRICT_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd.pdf"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "patna_rainfall.csv"

records = []

with pdfplumber.open(PDF_FILE) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""

        for line in text.splitlines():
            if re.search(r"\bPATNA\b", line, re.IGNORECASE):
                values = line.split()

                if len(values) >= 10:
                    records.append({
                        "district": "Patna",
                        "daily_actual_mm": values[2],
                        "daily_normal_mm": values[3],
                        "daily_departure_percent": values[4],
                        "daily_category": values[5],
                        "cumulative_actual_mm": values[6],
                        "cumulative_normal_mm": values[7],
                        "cumulative_departure_percent": values[8],
                        "cumulative_category": values[9],
                        "pdf_page": page_number
                    })

if records:
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print("CSV created successfully:", OUTPUT_FILE)
    print("Records extracted:", len(records))
else:
    print("No Patna records found.")
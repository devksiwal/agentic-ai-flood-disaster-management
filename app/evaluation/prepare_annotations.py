
import json
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "model_evaluation"
    / "humaid_kerala"
    / "train.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "model_evaluation"
    / "humaid_annotations.csv"
)

RELEVANT_LABELS = {
    "requests_or_urgent_needs",
    "injured_or_dead_people",
    "displaced_people_and_evacuations",
}

with open(SOURCE_FILE, "r", encoding="utf-8") as file:
    records = json.load(file)

selected_records = [
    record
    for record in records
    if record["class_label"] in RELEVANT_LABELS
]

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "tweet_id",
            "tweet_text",
            "original_label",
            "project_label",
            "review_notes",
        ],
    )

    writer.writeheader()

    for record in selected_records:
        writer.writerow({
            "tweet_id": record["tweet_id"],
            "tweet_text": record["tweet_text"],
            "original_label": record["class_label"],
            "project_label": "",
            "review_notes": "",
        })

print("Annotation dataset created successfully.")
print("Selected records:", len(selected_records))
print("Output file:", OUTPUT_FILE)

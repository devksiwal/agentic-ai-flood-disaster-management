
import json
from pathlib import Path

folder = Path("data/model_evaluation/humaid_kerala")

target_labels = [
    "requests_or_urgent_needs",
    "injured_or_dead_people",
    "displaced_people_and_evacuations",
]

with open(folder / "train.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for label in target_labels:
    print("\n" + "=" * 60)
    print("CATEGORY:", label)
    print("=" * 60)

    examples = [
        item["tweet_text"]
        for item in data
        if item["class_label"] == label
    ]

    for index, example in enumerate(examples[:10], start=1):
        print(f"\n{index}. {example}")

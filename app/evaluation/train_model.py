
from pathlib import Path
import time

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "model_evaluation"
    / "emergency_dataset.csv"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "data"
    / "model_evaluation"
    / "trained_model"
)

MODEL_PATH = MODEL_DIR / "emergency_classifier.joblib"


def main():
    print("Loading emergency dataset...")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    dataset = pd.read_csv(DATASET_PATH)

    required_columns = {"message", "emergency_type"}

    if not required_columns.issubset(dataset.columns):
        raise ValueError(
            "Dataset must contain message and emergency_type columns."
        )

    dataset = dataset.dropna(
        subset=["message", "emergency_type"]
    )

    if dataset["emergency_type"].nunique() < 2:
        raise ValueError(
            "At least two emergency categories are required."
        )

    X = dataset["message"].astype(str)
    y = dataset["emergency_type"].astype(str)

    print(f"Total examples: {len(dataset)}")
    print(f"Emergency categories: {sorted(y.unique())}")

    # TF-IDF + Logistic Regression pipeline
    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42,
            ),
        ),
    ])

    print("\nTraining model...")

    start_time = time.perf_counter()

    model.fit(X, y)

    training_time = time.perf_counter() - start_time

    # Save trained model
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print("\nTraining completed.")
    print(f"Training time: {training_time:.4f} seconds")
    print(f"Model saved to: {MODEL_PATH}")

    print("\nTesting sample predictions:")

    samples = [
        "Floodwater is entering our house",
        "Three people are trapped on a roof",
        "An injured person needs medical help",
        "We need to evacuate our village",
        "A child has been missing since the flood",
    ]

    for message in samples:
        prediction = model.predict([message])[0]
        print(f"{message} -> {prediction}")


if __name__ == "__main__":
    main()

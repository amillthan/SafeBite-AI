from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

DATA_PATH = Path("data/processed/synthetic_reviews.csv")
MODEL_PATH = Path("artifacts/models/food_safety_classifier.joblib")


def train_model():
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Validate dataset
    required_columns = {"text", "label"}

    if not required_columns.issubset(df.columns):
        raise ValueError("Dataset must contain text and label columns.")

    df = df.dropna(subset=["text", "label"])

    if not df["label"].isin([0, 1]).all():
        raise ValueError("Labels must be 0 or 1.")

    X = df["text"]
    y = df["label"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    # Create ML pipeline
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])

    # Train model
    model.fit(X_train, y_train)

    # Evaluate model
    predictions = model.predict(X_test)

    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions, labels=[0, 1]))

    # Save trained model
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved successfully: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
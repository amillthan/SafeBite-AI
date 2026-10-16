
from pathlib import Path

import joblib

from backend.app.services.category_service import detect_categories


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[3]

# Newly trained SafeBite AI model
MODEL_PATH = (
    BASE_DIR
    / "models"
    / "safebite_binary_model.joblib"
)

_model = None


def get_model():
    global _model

    if _model is None:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                f"Trained model not found: {MODEL_PATH}"
            )

        _model = joblib.load(MODEL_PATH)

    return _model


def predict_food_safety(review_text: str):

    if not isinstance(review_text, str) or not review_text.strip():
        raise ValueError("Review text cannot be empty")

    model = get_model()

    prediction = int(model.predict([review_text])[0])

    probabilities = model.predict_proba([review_text])[0]

    class_index = list(model.classes_).index(prediction)

    confidence = float(probabilities[class_index])

    label = (
        "Potential Food Safety Complaint"
        if prediction == 1
        else "No Food Safety Complaint"
    )

    # Categories are rule-based, not predicted by the ML model
    categories = (
        detect_categories(review_text)
        if prediction == 1
        else []
    )

    return {
        "prediction": prediction,
        "label": label,
        "confidence": confidence,
        "categories": categories,
    }
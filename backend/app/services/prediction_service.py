from pathlib import Path
from backend.app.services.category_service import detect_categories

import joblib

MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "artifacts"
    / "models"
    / "food_safety_classifier.joblib"
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

    categories = detect_categories(review_text)

    return {
        "prediction": prediction,
        "label": label,
        "confidence": confidence,
        "categories": categories,
    }
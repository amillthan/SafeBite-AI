
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "safebite_binary_model.joblib"

model = joblib.load(MODEL_PATH)

reviews = [
    "The chicken was raw and undercooked.",
    "I found a cockroach in my food.",
    "The food was delicious and fresh.",
    "The delivery was late but the food was good.",
    "I got sick and vomited after eating the meal.",
    "The restaurant was too expensive."
]

predictions = model.predict(reviews)
probabilities = model.predict_proba(reviews)

for review, prediction, probability in zip(
    reviews, predictions, probabilities
):
    confidence = probability[list(model.classes_).index(prediction)]

    print("\nReview:", review)
    print(
        "Prediction:",
        "Food Safety Complaint" if prediction == 1
        else "Not Food Safety"
    )
    print(f"Model confidence: {confidence:.2%}")

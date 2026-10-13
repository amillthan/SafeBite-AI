from backend.app.services.prediction_service import predict_food_safety


def analyze_reviews(reviews: list[str]) -> list[dict]:
    results = []

    for review in reviews:
        result = predict_food_safety(review)

        results.append({
            "review": review,
            "prediction": result["prediction"],
            "label": result["label"],
            "confidence": result["confidence"],
            "categories": result["categories"],
        })

    return results
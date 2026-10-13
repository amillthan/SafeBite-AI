from collections import defaultdict

from backend.app.services.warning_service import calculate_warning


def analyze_restaurants(results: list[dict]) -> list[dict]:
    grouped = defaultdict(list)

    for result in results:
        restaurant_id = result.get("restaurant_id")

        if restaurant_id:
            grouped[restaurant_id].append(result)

    summaries = []

    for restaurant_id, reviews in grouped.items():
        summary = calculate_warning(reviews)
        summary["restaurant_id"] = restaurant_id
        summaries.append(summary)

    return sorted(
        summaries,
        key=lambda item: (
            -item["complaint_rate"],
            item["restaurant_id"],
        ),
    )
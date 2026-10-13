from backend.app.services.restaurant_service import analyze_restaurants


def test_restaurant_grouping():
    results = [
        {
            "restaurant_id": "R001",
            "prediction": 1,
            "categories": ["Hygiene"],
        },
        {
            "restaurant_id": "R001",
            "prediction": 0,
            "categories": [],
        },
        {
            "restaurant_id": "R002",
            "prediction": 0,
            "categories": [],
        },
    ]

    summaries = analyze_restaurants(results)

    assert len(summaries) == 2

    by_id = {
        item["restaurant_id"]: item
        for item in summaries
    }

    assert by_id["R001"]["total_reviews"] == 2
    assert by_id["R001"]["flagged_reviews"] == 1
    assert by_id["R002"]["total_reviews"] == 1
    assert by_id["R002"]["flagged_reviews"] == 0
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_batch_prediction_success():
    with patch(
        "backend.app.services.batch_service.predict_food_safety"
    ) as mock_predict:
        mock_predict.return_value = {
            "prediction": 1,
            "label": "Potential Food Safety Complaint",
            "confidence": 0.8,
            "categories": ["Hygiene"],
        }

        response = client.post(
            "/api/predict/batch",
            json={
                "reviews": [
                    "The kitchen was filthy.",
                    "The restaurant was dirty.",
                ]
            },
        )

    assert response.status_code == 200
    assert response.json()["total_reviews"] == 2
    assert len(response.json()["results"]) == 2


def test_batch_prediction_empty_list():
    response = client.post(
        "/api/predict/batch",
        json={"reviews": []},
    )

    assert response.status_code == 422


def test_batch_prediction_empty_review():
    response = client.post(
        "/api/predict/batch",
        json={"reviews": [""]},
    )

    assert response.status_code == 422


def test_batch_prediction_missing_reviews():
    response = client.post(
        "/api/predict/batch",
        json={},
    )

    assert response.status_code == 422
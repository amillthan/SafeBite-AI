from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_prediction_api_success():
    response = client.post(
        "/api/predict",
        json={"text": "I found a cockroach in my food."},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] in [0, 1]
    assert isinstance(data["label"], str)
    assert 0 <= data["confidence"] <= 1


def test_prediction_api_empty_review():
    response = client.post(
        "/api/predict",
        json={"text": ""},
    )

    assert response.status_code == 422


def test_prediction_api_missing_text():
    response = client.post(
        "/api/predict",
        json={},
    )

    assert response.status_code == 422


def test_prediction_api_invalid_text_type():
    response = client.post(
        "/api/predict",
        json={"text": 123},
    )

    assert response.status_code == 422
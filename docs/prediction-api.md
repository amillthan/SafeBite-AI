# SafeBite AI — Food Safety Prediction API

## 1. Overview

The Food Safety Prediction API analyzes restaurant review text and predicts whether it contains a potential food safety complaint.

The API uses a machine learning model built with TF-IDF and Logistic Regression.

**Current status:** Prototype trained using synthetic reviews. Not suitable for production food safety decisions.

## 2. API Endpoint

**Method:** POST

**Endpoint:** `/api/predict`

**Content type:** `application/json`

## 3. Request Format

```json
{
  "text": "I found a cockroach in my food."
}
```

The `text` field is required and accepts a string containing 1–10,000 characters.

## 4. Response Format

Example response:

```json
{
  "prediction": 1,
  "label": "Potential Food Safety Complaint",
  "confidence": 0.5673
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `prediction` | Integer | `1` = potential food safety complaint; `0` = no complaint detected |
| `label` | String | Human-readable prediction |
| `confidence` | Float | Estimated probability of the predicted class, between 0 and 1 |

The confidence value is not a verified measure of real-world accuracy.

## 5. Model Information

- Feature extraction: TF-IDF
- Classification algorithm: Logistic Regression
- Model artifact: `artifacts/models/food_safety_classifier.joblib`
- Training script: `ml/train_baseline.py`
- Training dataset: `data/processed/synthetic_reviews.csv`

## 6. Backend Implementation

- Application: `backend/app/main.py`
- API router: `backend/app/routes/prediction_routes.py`
- Prediction service: `backend/app/services/prediction_service.py`

## 7. Input Validation

The API returns HTTP 422 when the request contains an empty review, omits the required `text` field, or provides an invalid input type.

## 8. Testing

Automated tests are located in `tests/test_prediction_api.py`.

The four tests verify successful API responses, empty review rejection, missing text rejection, and invalid text type rejection.

## 9. Limitations

- The model is trained on a very small synthetic dataset.
- Predictions are not verified food safety findings.
- Current performance is insufficient for real-world monitoring.
- A suitable labeled dataset and further evaluation are required before production use.
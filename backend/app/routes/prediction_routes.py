from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.services.prediction_service import predict_food_safety
router = APIRouter(prefix="/api", tags=["Prediction"])


class ReviewRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)


class PredictionResponse(BaseModel):
    prediction: int
    label: str
    confidence: float


@router.post("/predict", response_model=PredictionResponse)
def predict_review(request: ReviewRequest):
    return predict_food_safety(request.text)
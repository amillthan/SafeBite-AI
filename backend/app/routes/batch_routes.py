from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.services.batch_service import analyze_reviews
from backend.app.services.warning_service import calculate_warning
from backend.app.services.restaurant_service import analyze_restaurants

router = APIRouter(prefix="/api", tags=["Batch Analysis"])


class BatchRequest(BaseModel):
    reviews: list[str] = Field(min_length=1, max_length=1000)
    restaurant_ids: list[str] | None = None


@router.post("/predict/batch")
def predict_batch(request: BatchRequest):
    if any(not review.strip() or len(review) > 10000 for review in request.reviews):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail="Each review must contain 1 to 10000 non-whitespace characters.",
        )

    results = analyze_reviews(request.reviews)

    restaurant_summaries = []

    if request.restaurant_ids is not None:
        if (
            len(request.restaurant_ids) != len(request.reviews)
            or any(
                not isinstance(value, str) or not value.strip()
                for value in request.restaurant_ids
            )
        ):
            raise HTTPException(
                status_code=422,
                detail="Each review must have a valid restaurant ID.",
            )

        for result, restaurant_id in zip(
            results, request.restaurant_ids
        ):
            result["restaurant_id"] = restaurant_id

        restaurant_summaries = analyze_restaurants(results)

    return {
        "total_reviews": len(results),
        "results": results,
        "warning": calculate_warning(results),
        "restaurants": restaurant_summaries,
    }
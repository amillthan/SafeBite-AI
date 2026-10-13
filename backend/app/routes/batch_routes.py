from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.services.batch_service import analyze_reviews

router = APIRouter(prefix="/api", tags=["Batch Analysis"])


class BatchRequest(BaseModel):
    reviews: list[str] = Field(min_length=1, max_length=1000)


@router.post("/predict/batch")
def predict_batch(request: BatchRequest):
    if any(not review.strip() or len(review) > 10000 for review in request.reviews):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail="Each review must contain 1 to 10000 non-whitespace characters.",
        )

    results = analyze_reviews(request.reviews)

    return {
        "total_reviews": len(results),
        "results": results,
    }
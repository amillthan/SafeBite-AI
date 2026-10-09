from fastapi import FastAPI
from backend.app.routes.prediction_routes import router as prediction_router
app = FastAPI(
    title="SafeBite AI API",
    description="AI-Powered Food Safety Early Warning System",
    version="0.1.0"
)


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SafeBite AI Backend"
    }

app.include_router(prediction_router)
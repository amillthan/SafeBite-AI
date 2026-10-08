from fastapi import FastAPI

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
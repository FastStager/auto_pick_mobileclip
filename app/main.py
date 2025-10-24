from fastapi import FastAPI
from app.api.endpoints import staging

app = FastAPI(
    title="Virtual Staging Ranker API",
    description="An API to rank images based on their suitability for virtual staging using MobileCLIP2.",
    version="1.0.0"
)

app.include_router(staging.router, prefix="/api/v1", tags=["Staging"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Staging Ranker API. Visit /docs for more info."}

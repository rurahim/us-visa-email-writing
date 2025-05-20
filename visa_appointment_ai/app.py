from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(
    title="US Visa Appointment Prioritizer",
    description="AI system to prioritize visa emails based on urgency and rewrite for better impact.",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.api.tasks import router as tasks_router
from app.api.security import router as security_router


app = FastAPI(
    title="Aura AI",
    version="1.0.0",
    description=(
        "Aura autonomous AI orchestration and defensive "
        "security intelligence platform."
    )
)


origins = [
    origin.strip()
    for origin in settings.allowed_origins.split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(security_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": "Aura AI",
        "status": "online",
        "architecture": "orchestration"
    }
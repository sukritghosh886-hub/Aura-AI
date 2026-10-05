from fastapi import APIRouter

from app.models import ChatRequest
from app.core.orchestrator import run_objective

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):
    result = await run_objective(request.message)

    return {
        "user_id": request.user_id,
        **result
    }
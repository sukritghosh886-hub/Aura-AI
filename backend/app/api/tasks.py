from fastapi import APIRouter

from app.models import TaskRequest
from app.services.supabase import get_admin_client
from app.core.orchestrator import run_objective

router = APIRouter()


@router.post("/tasks")
async def create_task(request: TaskRequest):
    supabase = get_admin_client()

    task = supabase.table("tasks").insert({
        "user_id": request.user_id,
        "objective": request.objective,
        "priority": request.priority,
        "status": "planning"
    }).execute()

    result = await run_objective(request.objective)

    task_id = (
        task.data[0]["id"]
        if task.data
        else None
    )

    if task_id:
        supabase.table("tasks").update({
            "status": "completed"
        }).eq("id", task_id).execute()

    return {
        "task_id": task_id,
        "result": result
    }
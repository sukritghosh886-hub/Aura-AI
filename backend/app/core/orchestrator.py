from app.core.planner import create_plan
from app.core.verifier import verify_result
from app.services.ai_provider import generate_response


async def run_objective(objective: str) -> dict:
    plan = create_plan(objective)

    reasoning = await generate_response(
        f"""
Objective:
{objective}

Execution plan:
{plan}

Provide a concise operational response.
Do not claim that an action was executed unless it actually was.
"""
    )

    verification = verify_result(reasoning)

    return {
        "objective": objective,
        "plan": plan,
        "response": reasoning,
        "verification": verification
    }
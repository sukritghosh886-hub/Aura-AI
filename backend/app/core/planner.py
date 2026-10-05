from typing import Any


def create_plan(objective: str) -> list[dict[str, Any]]:
    objective_lower = objective.lower()

    steps = []

    steps.append({
        "step": 1,
        "action": "understand_objective",
        "description": "Interpret the requested objective.",
        "risk": "low"
    })

    if any(word in objective_lower for word in [
        "security",
        "cybersecurity",
        "vulnerability",
        "glitch",
        "audit"
    ]):
        steps.append({
            "step": 2,
            "action": "authorization_check",
            "description": (
                "Confirm that the target is owned or explicitly "
                "authorized for security assessment."
            ),
            "risk": "low"
        })

        steps.append({
            "step": 3,
            "action": "defensive_audit",
            "description": (
                "Perform non-destructive security checks "
                "against the authorized target."
            ),
            "risk": "low"
        })

    else:
        steps.append({
            "step": 2,
            "action": "context_collection",
            "description": "Collect relevant Aura memory and task context.",
            "risk": "low"
        })

        steps.append({
            "step": 3,
            "action": "execute_authorized_tools",
            "description": "Execute only permitted tools.",
            "risk": "medium"
        })

    steps.append({
        "step": len(steps) + 1,
        "action": "verify",
        "description": "Check the result before reporting it.",
        "risk": "low"
    })

    return steps
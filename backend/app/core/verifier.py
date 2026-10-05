from typing import Any


def verify_result(result: Any) -> dict:
    if result is None:
        return {
            "verified": False,
            "reason": "No result was produced."
        }

    return {
        "verified": True,
        "reason": "Result exists and passed the basic orchestration check."
    }
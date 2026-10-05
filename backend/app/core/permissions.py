from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def classify_action(action: str) -> RiskLevel:
    action = action.lower()

    if any(word in action for word in [
        "delete",
        "transfer",
        "purchase",
        "send money",
        "change password"
    ]):
        return RiskLevel.HIGH

    if any(word in action for word in [
        "scan",
        "audit",
        "analyze",
        "inspect",
        "check"
    ]):
        return RiskLevel.LOW

    return RiskLevel.MEDIUM


def requires_approval(action: str) -> bool:
    risk = classify_action(action)

    return risk in {
        RiskLevel.HIGH,
        RiskLevel.CRITICAL
    }
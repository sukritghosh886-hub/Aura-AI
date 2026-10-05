from typing import Any


def check_authorization(authorization_confirmed: bool) -> dict[str, Any]:
    if not authorization_confirmed:
        return {
            "severity": "high",
            "category": "authorization",
            "title": "Authorization not confirmed",
            "description": (
                "The requested security assessment does not have "
                "confirmed authorization."
            ),
            "recommendation": (
                "Confirm ownership or explicit authorization before "
                "performing the assessment."
            ),
            "evidence": {}
        }

    return {
        "severity": "info",
        "category": "authorization",
        "title": "Authorization confirmed",
        "description": "The user confirmed authorized assessment.",
        "recommendation": "Continue with permitted defensive checks.",
        "evidence": {}
    }


def basic_configuration_checks(target_type: str) -> list[dict[str, Any]]:
    findings = []

    if target_type == "web_app":
        findings.append({
            "severity": "low",
            "category": "configuration",
            "title": "Security configuration review required",
            "description": (
                "Aura recommends reviewing HTTPS, security headers, "
                "authentication, session handling, and dependency versions."
            ),
            "recommendation": (
                "Run a complete authorized security review and "
                "remediate confirmed weaknesses."
            ),
            "evidence": {
                "check": "configuration_review"
            }
        })

    elif target_type == "api":
        findings.append({
            "severity": "low",
            "category": "api_security",
            "title": "API authorization review required",
            "description": (
                "Review authentication, authorization, rate limiting, "
                "input validation, and secret handling."
            ),
            "recommendation": (
                "Verify every protected endpoint enforces authorization."
            ),
            "evidence": {
                "check": "api_security_review"
            }
        })

    else:
        findings.append({
            "severity": "info",
            "category": "general",
            "title": "Baseline security assessment",
            "description": (
                "Aura created a defensive baseline assessment."
            ),
            "recommendation": (
                "Add target-specific authorized checks."
            ),
            "evidence": {}
        })

    return findings
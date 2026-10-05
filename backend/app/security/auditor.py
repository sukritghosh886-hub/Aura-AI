from app.security.checks import (
    check_authorization,
    basic_configuration_checks
)
from app.security.risk import calculate_risk


def run_security_audit(
    target_name: str,
    target_type: str,
    authorization_confirmed: bool
) -> dict:

    findings = []

    authorization = check_authorization(
        authorization_confirmed
    )

    findings.append(authorization)

    if authorization_confirmed:
        findings.extend(
            basic_configuration_checks(target_type)
        )

    risk_score = calculate_risk(findings)

    return {
        "target_name": target_name,
        "target_type": target_type,
        "risk_score": risk_score,
        "findings": findings
    }
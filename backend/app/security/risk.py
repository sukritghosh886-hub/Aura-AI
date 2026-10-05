SEVERITY_SCORE = {
    "info": 0,
    "low": 1,
    "medium": 3,
    "high": 7,
    "critical": 10
}


def calculate_risk(findings: list[dict]) -> int:
    score = sum(
        SEVERITY_SCORE.get(
            finding.get("severity", "info"),
            0
        )
        for finding in findings
    )

    return min(score, 100)
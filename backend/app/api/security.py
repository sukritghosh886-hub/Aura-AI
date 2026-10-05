from fastapi import APIRouter, HTTPException

from app.models import SecurityScanRequest
from app.security.auditor import run_security_audit
from app.services.supabase import get_admin_client

router = APIRouter()


@router.post("/security/scan")
async def security_scan(request: SecurityScanRequest):
    if not request.authorization_confirmed:
        raise HTTPException(
            status_code=403,
            detail=(
                "Authorization must be confirmed before "
                "performing a security assessment."
            )
        )

    result = run_security_audit(
        target_name=request.target_name,
        target_type=request.target_type,
        authorization_confirmed=request.authorization_confirmed
    )

    supabase = get_admin_client()

    scan = supabase.table("security_scans").insert({
        "user_id": request.user_id,
        "target_name": request.target_name,
        "target_type": request.target_type,
        "authorization_confirmed": True,
        "status": "completed",
        "risk_score": result["risk_score"],
        "summary": "Defensive security baseline completed.",
        "findings": result["findings"]
    }).execute()

    scan_id = scan.data[0]["id"]

    for finding in result["findings"]:
        supabase.table("security_findings").insert({
            "scan_id": scan_id,
            "severity": finding["severity"],
            "category": finding["category"],
            "title": finding["title"],
            "description": finding["description"],
            "recommendation": finding["recommendation"],
            "evidence": finding["evidence"]
        }).execute()

    return {
        "scan_id": scan_id,
        "status": "completed",
        **result
    }
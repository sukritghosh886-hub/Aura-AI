from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    user_id: str


class TaskRequest(BaseModel):
    objective: str = Field(min_length=1, max_length=5000)
    user_id: str
    priority: int = Field(default=5, ge=1, le=10)


class SecurityScanRequest(BaseModel):
    user_id: str
    target_name: str
    target_type: str
    authorization_confirmed: bool


class SecurityFinding(BaseModel):
    severity: str
    category: str
    title: str
    description: str
    recommendation: str
    evidence: dict[str, Any] = {}


class SecurityScanResponse(BaseModel):
    scan_id: str
    status: str
    findings: list[SecurityFinding]
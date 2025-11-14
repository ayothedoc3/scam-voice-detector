from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StartProtectionRequest(BaseModel):
    user_phone: str


class StartProtectionResponse(BaseModel):
    session_id: int
    call_sid: str
    bridge_number: str
    instructions: str


class StopProtectionRequest(BaseModel):
    call_sid: str


class CallStatusResponse(BaseModel):
    call_sid: str
    status: str
    current_risk_score: float
    duration: float


class CallSessionResponse(BaseModel):
    id: int
    call_sid: str
    status: str
    phone_number: Optional[str]
    started_at: datetime
    ended_at: Optional[datetime]
    total_duration: float
    max_risk_score: float
    final_verdict: Optional[str]

    class Config:
        from_attributes = True

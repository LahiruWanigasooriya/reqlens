import uuid
from datetime import datetime

from pydantic import BaseModel


class CriterionResponse(BaseModel):
    id: uuid.UUID
    criterion_number: int
    description: str
    expected_behavior: str | None
    constraint_text: str | None


class RequirementResponse(BaseModel):
    id: uuid.UUID
    external_id: str
    title: str
    description: str
    requirement_type: str
    source_text: str | None
    created_at: datetime
    criteria: list[CriterionResponse]
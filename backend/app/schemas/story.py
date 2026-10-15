import uuid

from pydantic import BaseModel


class AcceptanceCriterionResponse(BaseModel):
    id: uuid.UUID
    criterion_number: int
    description: str


class UserStoryResponse(BaseModel):
    id: uuid.UUID

    external_id: str

    title: str

    description: str | None

    issue_type: str

    status: str

    requirement_id: uuid.UUID | None

    requirement_external_id: str | None

    acceptance_criteria: list[
        AcceptanceCriterionResponse
    ]
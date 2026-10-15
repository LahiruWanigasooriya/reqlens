from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):

    query: str = Field(
        min_length=2,
    )

    top_k: int = Field(
        default=8,
        ge=1,
        le=30,
    )

    evidence_types: list[str] | None = None
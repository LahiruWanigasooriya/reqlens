from pydantic import BaseModel, Field


class ExtractedCriterion(BaseModel):
    description: str = Field(
        description=(
            "A single atomic statement that can "
            "be independently verified."
        )
    )

    expected_behavior: str | None = Field(
        default=None,
        description=(
            "The expected system behavior."
        ),
    )

    constraint_text: str | None = Field(
        default=None,
        description=(
            "Explicit constraint such as time, "
            "size, role, limit, state or value."
        ),
    )


class ExtractedRequirement(BaseModel):
    external_id: str = Field(
        description=(
            "Requirement identifier such as REQ-001."
        )
    )

    title: str

    description: str

    requirement_type: str = Field(
        description=(
            "functional, non_functional, "
            "business_rule, security, "
            "performance or other"
        )
    )

    source_text: str

    criteria: list[ExtractedCriterion]


class RequirementExtractionResult(BaseModel):
    requirements: list[ExtractedRequirement]
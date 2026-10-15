from typing import Literal

from pydantic import BaseModel, Field


EvidenceStrength = Literal[
    "strong",
    "moderate",
    "weak",
    "irrelevant",
]


class CandidateEvidenceInput(BaseModel):
    candidate_id: str
    source_name: str
    evidence_type: str
    content: str


class EvidenceAssessment(BaseModel):
    candidate_id: str

    relevant: bool = Field(
        description=(
            "Whether this candidate is genuinely "
            "relevant to the criterion."
        )
    )

    supports_criterion: bool = Field(
        description=(
            "Whether the candidate provides evidence "
            "supporting the requested behavior."
        )
    )

    strength: EvidenceStrength

    relevance_score: float = Field(
        ge=0,
        le=1,
    )

    extracted_fact: str | None = Field(
        default=None,
        description=(
            "Concrete fact demonstrated by the evidence. "
            "Preserve important values and constraints."
        ),
    )

    explanation: str = Field(
        description=(
            "Short explanation of what this evidence "
            "does or does not establish."
        )
    )


class EvidenceAssessmentResult(BaseModel):
    assessments: list[EvidenceAssessment]
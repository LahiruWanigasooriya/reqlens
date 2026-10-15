from app.models.requirement import Requirement
from app.models.verifiable_criterion import (
    VerifiableCriterion,
)


def build_evidence_query(
    requirement: Requirement,
    criterion: VerifiableCriterion,
) -> str:

    parts = [
        requirement.title,
        requirement.description,
        criterion.description,
    ]

    if criterion.expected_behavior:
        parts.append(
            criterion.expected_behavior
        )

    if criterion.constraint_text:
        parts.append(
            criterion.constraint_text
        )

    return "\n".join(
        part.strip()
        for part in parts
        if part and part.strip()
    )
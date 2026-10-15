import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.evidence import Evidence
from app.models.requirement import Requirement
from app.models.verifiable_criterion import (
    VerifiableCriterion,
)


def get_requirement_evidence_summary(
    db: Session,
    project_id: uuid.UUID,
    requirement_id: uuid.UUID,
):

    requirement = db.scalar(
        select(Requirement).where(
            Requirement.id
            == requirement_id,

            Requirement.project_id
            == project_id,
        )
    )

    if not requirement:
        raise ValueError(
            "Requirement not found"
        )

    criteria = db.scalars(
        select(
            VerifiableCriterion
        )
        .where(
            VerifiableCriterion.requirement_id
            == requirement.id
        )
        .order_by(
            VerifiableCriterion.criterion_number
        )
    ).all()

    result = []

    for criterion in criteria:

        evidence = db.scalars(
            select(Evidence).where(
                Evidence.criterion_id
                == criterion.id
            )
        ).all()

        source = [
            item
            for item in evidence
            if item.evidence_type
            == "source"
            and item.strength
            in {"strong", "moderate"}
        ]

        tests = [
            item
            for item in evidence
            if item.evidence_type
            == "test"
            and item.strength
            in {"strong", "moderate"}
        ]

        docs = [
            item
            for item in evidence
            if item.evidence_type
            == "documentation"
            and item.strength
            in {"strong", "moderate"}
        ]

        stories = [
            item
            for item in evidence
            if item.evidence_type
            == "story"
            and item.strength
            in {"strong", "moderate"}
        ]

        result.append(
            {
                "criterion_number":
                    criterion.criterion_number,

                "criterion":
                    criterion.description,

                "implementation_evidence":
                    len(source),

                "test_evidence":
                    len(tests),

                "documentation_evidence":
                    len(docs),

                "story_evidence":
                    len(stories),

                "has_implementation_evidence":
                    bool(source),

                "has_test_evidence":
                    bool(tests),
            }
        )

    return {
        "requirement":
            requirement.external_id,

        "criteria":
            result,
    }
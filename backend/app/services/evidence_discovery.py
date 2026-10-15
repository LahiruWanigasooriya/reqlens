import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.ai.chains.evidence_assessment import (
    build_evidence_assessment_chain,
    serialize_candidates,
)
from app.models.evidence import Evidence
from app.models.requirement import Requirement
from app.models.verifiable_criterion import (
    VerifiableCriterion,
)
from app.services.evidence_query import (
    build_evidence_query,
)
from app.services.knowledge_retrieval import (
    retrieve_project_evidence,
)


SEARCH_TYPES = [
    "source",
    "test",
    "documentation",
    "story",
]


async def discover_criterion_evidence(
    db: Session,
    project_id: uuid.UUID,
    requirement: Requirement,
    criterion: VerifiableCriterion,
):

    query = build_evidence_query(
        requirement,
        criterion,
    )

    candidates = []

    for evidence_type in SEARCH_TYPES:

        results = retrieve_project_evidence(
            project_id=project_id,
            query=query,
            top_k=6,
            evidence_types=[
                evidence_type
            ],
        )

        candidates.extend(results)

    unique_candidates = {}

    for candidate in candidates:

        unique_candidates[
            candidate["vector_id"]
        ] = candidate

    candidates = list(
        unique_candidates.values()
    )

    db.execute(
        delete(Evidence).where(
            Evidence.criterion_id
            == criterion.id
        )
    )

    if not candidates:
        db.commit()

        return {
            "criterion_id":
                str(criterion.id),

            "candidates_found": 0,

            "evidence_kept": 0,
        }

    chain = (
        build_evidence_assessment_chain()
    )

    result = await chain.ainvoke(
        {
            "requirement":
                (
                    f"{requirement.external_id}: "
                    f"{requirement.title}\n"
                    f"{requirement.description}"
                ),

            "criterion":
                criterion.description,

            "candidates":
                serialize_candidates(
                    candidates
                ),
        }
    )

    candidate_map = {
        candidate["vector_id"]:
            candidate
        for candidate in candidates
    }

    kept = 0

    for assessment in result.assessments:

        candidate = candidate_map.get(
            assessment.candidate_id
        )

        if not candidate:
            continue

        if (
            not assessment.relevant
            or assessment.strength
            == "irrelevant"
        ):
            continue

        project_file_id = (
            candidate.get(
                "project_file_id"
            )
        )

        db.add(
            Evidence(
                project_id=project_id,

                requirement_id=
                    requirement.id,

                criterion_id=
                    criterion.id,

                project_file_id=(
                    uuid.UUID(
                        project_file_id
                    )
                    if project_file_id
                    else None
                ),

                vector_id=
                    candidate["vector_id"],

                source_name=
                    candidate["source_name"],

                evidence_type=
                    candidate["evidence_type"],

                content=
                    candidate["content"],

                relevance_score=
                    assessment.relevance_score,

                semantic_score=
                    candidate["score"],

                strength=
                    assessment.strength,

                supports_criterion=
                    assessment.supports_criterion,

                explanation=
                    assessment.explanation,

                extracted_fact=
                    assessment.extracted_fact,
            )
        )

        kept += 1

    db.commit()

    return {
        "criterion_id":
            str(criterion.id),

        "candidates_found":
            len(candidates),

        "evidence_kept":
            kept,
    }


async def discover_requirement_evidence(
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

    results = []

    for criterion in criteria:

        result = await (
            discover_criterion_evidence(
                db,
                project_id,
                requirement,
                criterion,
            )
        )

        results.append(result)

    return {
        "requirement":
            requirement.external_id,

        "criteria_analyzed":
            len(criteria),

        "results":
            results,
    }


async def discover_project_evidence(
    db: Session,
    project_id: uuid.UUID,
):

    requirements = db.scalars(
        select(Requirement)
        .where(
            Requirement.project_id
            == project_id
        )
        .order_by(
            Requirement.external_id
        )
    ).all()

    results = []

    for requirement in requirements:

        result = await (
            discover_requirement_evidence(
                db,
                project_id,
                requirement.id,
            )
        )

        results.append(result)

    return {
        "requirements_analyzed":
            len(requirements),

        "results":
            results,
    }
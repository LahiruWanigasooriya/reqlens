import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
)
from app.core.database import get_db
from app.models.evidence import Evidence
from app.models.requirement import Requirement
from app.models.user import User
from app.models.verifiable_criterion import (
    VerifiableCriterion,
)
from app.services.evidence_discovery import (
    discover_project_evidence,
    discover_requirement_evidence,
)
from app.services.project_access import (
    get_owned_project,
)

from app.services.evidence_summary import (
    get_requirement_evidence_summary,
)



router = APIRouter(
    prefix="/projects",
    tags=["Evidence"],
)


@router.post(
    "/{project_id}/requirements/{requirement_id}/discover-evidence"
)
async def discover_requirement(
    project_id: uuid.UUID,
    requirement_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    get_owned_project(
        db,
        current_user,
        project_id,
    )

    try:

        return await (
            discover_requirement_evidence(
                db,
                project_id,
                requirement_id,
            )
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{project_id}/evidence/discover"
)
async def discover_all_evidence(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    get_owned_project(
        db,
        current_user,
        project_id,
    )

    return await (
        discover_project_evidence(
            db,
            project_id,
        )
    )


@router.get(
    "/{project_id}/requirements/{requirement_id}/evidence"
)
def list_requirement_evidence(
    project_id: uuid.UUID,
    requirement_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    get_owned_project(
        db,
        current_user,
        project_id,
    )

    requirement = db.scalar(
        select(Requirement).where(
            Requirement.id
            == requirement_id,

            Requirement.project_id
            == project_id,
        )
    )

    if not requirement:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found",
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
            select(Evidence)
            .where(
                Evidence.criterion_id
                == criterion.id
            )
            .order_by(
                Evidence.relevance_score.desc()
            )
        ).all()

        result.append(
            {
                "criterion_id":
                    str(criterion.id),

                "criterion_number":
                    criterion.criterion_number,

                "criterion":
                    criterion.description,

                "evidence": [
                    {
                        "id":
                            str(item.id),

                        "source_name":
                            item.source_name,

                        "evidence_type":
                            item.evidence_type,

                        "strength":
                            item.strength,

                        "supports_criterion":
                            item.supports_criterion,

                        "relevance_score":
                            item.relevance_score,

                        "semantic_score":
                            item.semantic_score,

                        "extracted_fact":
                            item.extracted_fact,

                        "explanation":
                            item.explanation,

                        "content":
                            item.content,
                    }

                    for item in evidence
                ],
            }
        )

    return {
        "requirement":
            requirement.external_id,

        "criteria":
            result,
    }


@router.get(
    "/{project_id}/requirements/{requirement_id}/evidence-summary"
)
def evidence_summary(
    project_id: uuid.UUID,
    requirement_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    get_owned_project(
        db,
        current_user,
        project_id,
    )

    try:

        return (
            get_requirement_evidence_summary(
                db,
                project_id,
                requirement_id,
            )
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
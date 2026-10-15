import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.project_file import ProjectFile
from app.models.requirement import Requirement
from app.models.user import User
from app.models.verifiable_criterion import (
    VerifiableCriterion,
)
from app.services.project_access import (
    get_owned_project,
)
from app.services.requirement_extraction import (
    extract_requirements_from_file,
)
from app.models.user_story import UserStory


router = APIRouter(
    prefix="/projects",
    tags=["Requirements"],
)


@router.post(
    "/{project_id}/files/{file_id}/extract-requirements"
)
async def extract_requirements(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
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

    file = db.scalar(
        select(ProjectFile).where(
            ProjectFile.id == file_id,
            ProjectFile.project_id
            == project_id,
        )
    )

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    try:

        return await (
            extract_requirements_from_file(
                db,
                project_id,
                file_id,
            )
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{project_id}/requirements"
)
def list_requirements(
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

    result = []

    for requirement in requirements:

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

        result.append(
            {
                "id":
                    str(requirement.id),

                "external_id":
                    requirement.external_id,

                "title":
                    requirement.title,

                "description":
                    requirement.description,

                "requirement_type":
                    requirement.requirement_type,

                "source_text":
                    requirement.source_text,

                "created_at":
                    requirement.created_at,

                "criteria": [
                    {
                        "id":
                            str(criterion.id),

                        "criterion_number":
                            criterion.criterion_number,

                        "description":
                            criterion.description,

                        "expected_behavior":
                            criterion.expected_behavior,

                        "constraint_text":
                            criterion.constraint_text,
                    }

                    for criterion
                    in criteria
                ],
            }
        )

    return result


@router.get(
    "/{project_id}/traceability-summary"
)
def traceability_summary(
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

    requirements = db.scalars(
        select(Requirement).where(
            Requirement.project_id
            == project_id
        )
    ).all()

    results = []

    linked = 0

    for requirement in requirements:

        stories = db.scalars(
            select(UserStory).where(
                UserStory.project_id
                == project_id,

                UserStory.requirement_id
                == requirement.id,
            )
        ).all()

        has_story = len(stories) > 0

        if has_story:
            linked += 1

        results.append(
            {
                "requirement":
                    requirement.external_id,

                "has_story":
                    has_story,

                "stories": [
                    story.external_id
                    for story in stories
                ],
            }
        )

    total = len(requirements)

    coverage = (
        round(
            linked / total * 100,
            2,
        )
        if total
        else 0
    )

    return {
        "total_requirements":
            total,

        "requirements_with_story":
            linked,

        "requirements_without_story":
            total - linked,

        "story_traceability_coverage":
            coverage,

        "requirements":
            results,
    }
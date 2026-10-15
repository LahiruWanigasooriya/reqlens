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
from app.models.acceptance_criterion import (
    AcceptanceCriterion,
)
from app.models.project_file import ProjectFile
from app.models.requirement import Requirement
from app.models.user import User
from app.models.user_story import UserStory
from app.services.project_access import (
    get_owned_project,
)
from app.services.story_importer import (
    import_stories_from_file,
)


router = APIRouter(
    prefix="/projects",
    tags=["User Stories"],
)


@router.post(
    "/{project_id}/files/{file_id}/import-stories"
)
def import_stories(
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

        return import_stories_from_file(
            db,
            project_id,
            file_id,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{project_id}/stories"
)
def list_stories(
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

    stories = db.scalars(
        select(UserStory)
        .where(
            UserStory.project_id
            == project_id
        )
        .order_by(
            UserStory.external_id
        )
    ).all()

    result = []

    for story in stories:

        criteria = db.scalars(
            select(
                AcceptanceCriterion
            )
            .where(
                AcceptanceCriterion.story_id
                == story.id
            )
            .order_by(
                AcceptanceCriterion.criterion_number
            )
        ).all()

        requirement_external_id = None

        if story.requirement_id:

            requirement = db.get(
                Requirement,
                story.requirement_id,
            )

            if requirement:
                requirement_external_id = (
                    requirement.external_id
                )

        result.append(
            {
                "id": str(story.id),

                "external_id":
                    story.external_id,

                "title":
                    story.title,

                "description":
                    story.description,

                "issue_type":
                    story.issue_type,

                "status":
                    story.status,

                "requirement_id": (
                    str(story.requirement_id)
                    if story.requirement_id
                    else None
                ),

                "requirement_external_id":
                    requirement_external_id,

                "acceptance_criteria": [
                    {
                        "id":
                            str(criterion.id),

                        "criterion_number":
                            criterion.criterion_number,

                        "description":
                            criterion.description,
                    }

                    for criterion
                    in criteria
                ],
            }
        )

    return result
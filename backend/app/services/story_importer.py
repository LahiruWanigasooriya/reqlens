import json
import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.acceptance_criterion import (
    AcceptanceCriterion,
)
from app.models.project_file import ProjectFile
from app.models.requirement import Requirement
from app.models.user_story import UserStory


def import_stories_from_file(
    db: Session,
    project_id: uuid.UUID,
    file_id: uuid.UUID,
):

    project_file = db.scalar(
        select(ProjectFile).where(
            ProjectFile.id == file_id,
            ProjectFile.project_id == project_id,
        )
    )

    if not project_file:
        raise ValueError(
            "Project file not found"
        )

    if (
        project_file.processing_status
        != "ready"
    ):
        raise ValueError(
            "Project file is not ready"
        )

    if not project_file.extracted_text:
        raise ValueError(
            "File contains no content"
        )

    try:
        data = json.loads(
            project_file.extracted_text
        )

    except json.JSONDecodeError:
        raise ValueError(
            "Story file must contain valid JSON"
        )

    issues = data.get("issues", [])

    imported = []
    missing_requirement_links = []

    for issue in issues:

        external_id = issue.get("key")

        if not external_id:
            continue

        requirement_external_id = (
            issue.get("requirement_id")
        )

        requirement = None

        if requirement_external_id:

            requirement = db.scalar(
                select(Requirement).where(
                    Requirement.project_id
                    == project_id,

                    Requirement.external_id
                    == requirement_external_id,
                )
            )

        story = db.scalar(
            select(UserStory).where(
                UserStory.project_id
                == project_id,

                UserStory.external_id
                == external_id,
            )
        )

        if story:

            db.execute(
                delete(
                    AcceptanceCriterion
                ).where(
                    AcceptanceCriterion.story_id
                    == story.id
                )
            )

            story.source_file_id = file_id

            story.requirement_id = (
                requirement.id
                if requirement
                else None
            )

            story.title = issue.get(
                "title",
                external_id,
            )

            story.description = issue.get(
                "description"
            )

            story.issue_type = issue.get(
                "type",
                "Story",
            )

            story.status = issue.get(
                "status",
                "Unknown",
            )

        else:

            story = UserStory(
                project_id=project_id,

                source_file_id=file_id,

                requirement_id=(
                    requirement.id
                    if requirement
                    else None
                ),

                external_id=external_id,

                title=issue.get(
                    "title",
                    external_id,
                ),

                description=issue.get(
                    "description"
                ),

                issue_type=issue.get(
                    "type",
                    "Story",
                ),

                status=issue.get(
                    "status",
                    "Unknown",
                ),
            )

            db.add(story)
            db.flush()

        criteria = issue.get(
            "acceptance_criteria",
            [],
        )

        for number, description in enumerate(
            criteria,
            start=1,
        ):

            db.add(
                AcceptanceCriterion(
                    story_id=story.id,
                    criterion_number=number,
                    description=description,
                )
            )

        imported.append(external_id)

        if (
            requirement_external_id
            and not requirement
        ):
            missing_requirement_links.append(
                {
                    "story": external_id,
                    "requirement":
                        requirement_external_id,
                }
            )

    db.commit()

    return {
        "stories_imported":
            len(imported),

        "story_ids":
            imported,

        "unresolved_requirement_links":
            missing_requirement_links,
    }
import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.ai.chains.requirement_extraction import (
    build_requirement_extraction_chain,
)
from app.models.project_file import ProjectFile
from app.models.requirement import Requirement
from app.models.verifiable_criterion import (
    VerifiableCriterion,
)


async def extract_requirements_from_file(
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
            "Project file contains no extracted text"
        )

    chain = build_requirement_extraction_chain()

    result = await chain.ainvoke(
        {
            "document":
                project_file.extracted_text
        }
    )

    extracted_ids = []

    for item in result.requirements:

        existing = db.scalar(
            select(Requirement).where(
                Requirement.project_id
                == project_id,

                Requirement.external_id
                == item.external_id,
            )
        )

        if existing:

            db.execute(
                delete(
                    VerifiableCriterion
                ).where(
                    VerifiableCriterion.requirement_id
                    == existing.id
                )
            )

            existing.source_file_id = (
                file_id
            )

            existing.title = item.title

            existing.description = (
                item.description
            )

            existing.requirement_type = (
                item.requirement_type
            )

            existing.source_text = (
                item.source_text
            )

            requirement = existing

        else:

            requirement = Requirement(
                project_id=project_id,
                source_file_id=file_id,
                external_id=
                    item.external_id,
                title=item.title,
                description=
                    item.description,
                requirement_type=
                    item.requirement_type,
                source_text=
                    item.source_text,
            )

            db.add(requirement)

            db.flush()

        for number, criterion in enumerate(
            item.criteria,
            start=1,
        ):

            db.add(
                VerifiableCriterion(
                    requirement_id=
                        requirement.id,

                    criterion_number=
                        number,

                    description=
                        criterion.description,

                    expected_behavior=
                        criterion.expected_behavior,

                    constraint_text=
                        criterion.constraint_text,
                )
            )

        extracted_ids.append(
            requirement.external_id
        )

    db.commit()

    return {
        "file_id": str(file_id),
        "requirements_found":
            len(result.requirements),
        "requirement_ids":
            extracted_ids,
    }
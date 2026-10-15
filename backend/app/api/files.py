import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.project_file import ProjectFile
from app.models.user import User
from app.schemas.project_file import ProjectFileResponse
from app.services.file_parser import (
    SUPPORTED_EXTENSIONS,
    extract_text,
)
from app.services.file_storage import save_upload
from app.services.project_access import get_owned_project
from app.services.evidence_classifier import classify_file
from app.services.evidence_classifier import classify_file


router = APIRouter(
    prefix="/projects",
    tags=["Project Files"],
)


@router.post(
    "/{project_id}/files",
    response_model=ProjectFileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_project_file(
    project_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_project(
        db,
        current_user,
        project_id,
    )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type: {extension}"
            ),
        )

    try:
        path, stored_name, size = (
            await save_upload(
                project_id,
                file,
            )
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(exc),
        )

    project_file = ProjectFile(
        project_id=project_id,
        original_name=file.filename,
        stored_name=stored_name,
        file_type=extension.lstrip("."),
        mime_type=file.content_type,
        size_bytes=size,
        storage_path=str(path),

        evidence_type=classify_file(
            file.filename,
        ),

        processing_status="processing",
    )

    db.add(project_file)
    db.commit()
    db.refresh(project_file)

    try:
        extracted = extract_text(path)

        project_file.extracted_text = extracted
        project_file.processing_status = "ready"
        project_file.processing_error = None

    except Exception as exc:
        project_file.processing_status = "failed"
        project_file.processing_error = str(exc)

    db.commit()
    db.refresh(project_file)

    return project_file


@router.get(
    "/{project_id}/files",
    response_model=list[ProjectFileResponse],
)
def list_project_files(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_project(
        db,
        current_user,
        project_id,
    )

    files = db.scalars(
        select(ProjectFile)
        .where(
            ProjectFile.project_id
            == project_id
        )
        .order_by(
            ProjectFile.created_at.desc()
        )
    ).all()

    return files

@router.get(
    "/{project_id}/files/{file_id}/content",
)
def get_file_content(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_project(
        db,
        current_user,
        project_id,
    )

    project_file = db.scalar(
        select(ProjectFile).where(
            ProjectFile.id == file_id,
            ProjectFile.project_id == project_id,
        )
    )

    if not project_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return {
        "id": str(project_file.id),
        "name": project_file.original_name,
        "status": project_file.processing_status,
        "content": project_file.extracted_text,
    }

@router.delete(
    "/{project_id}/files/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_file(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_project(
        db,
        current_user,
        project_id,
    )

    project_file = db.scalar(
        select(ProjectFile).where(
            ProjectFile.id == file_id,
            ProjectFile.project_id == project_id,
        )
    )

    if not project_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    path = Path(project_file.storage_path)

    if path.exists():
        path.unlink()

    db.delete(project_file)
    db.commit()

    return None


@router.post(
    "/{project_id}/files/reclassify"
)
def reclassify_project_files(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_project(
        db,
        current_user,
        project_id,
    )

    files = db.scalars(
        select(ProjectFile).where(
            ProjectFile.project_id
            == project_id
        )
    ).all()

    results = []

    for project_file in files:

        project_file.evidence_type = (
            classify_file(
                project_file.original_name,
                project_file.extracted_text,
            )
        )

        results.append(
            {
                "file":
                    project_file.original_name,

                "evidence_type":
                    project_file.evidence_type,
            }
        )

    db.commit()

    return {
        "classified": len(results),
        "files": results,
    }
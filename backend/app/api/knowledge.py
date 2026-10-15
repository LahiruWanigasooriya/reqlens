import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
)
from app.core.database import get_db
from app.models.knowledge_chunk import (
    KnowledgeChunk,
)
from app.models.user import User
from app.schemas.knowledge import (
    RetrievalRequest,
)
from app.services.knowledge_index import (
    build_project_knowledge_index,
)
from app.services.knowledge_retrieval import (
    retrieve_project_evidence,
)
from app.services.project_access import (
    get_owned_project,
)


router = APIRouter(
    prefix="/projects",
    tags=["Project Knowledge"],
)


@router.post(
    "/{project_id}/knowledge/build"
)
def build_knowledge(
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

    try:

        result = (
            build_project_knowledge_index(
                db,
                project_id,
            )
        )

        return {
            "status": "ready",
            **result,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{project_id}/knowledge/status"
)
def knowledge_status(
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

    count = db.scalar(
        select(
            func.count(
                KnowledgeChunk.id
            )
        ).where(
            KnowledgeChunk.project_id
            == project_id
        )
    )

    return {
        "ready": bool(count),
        "chunks": count or 0,
    }


@router.post(
    "/{project_id}/knowledge/search"
)
def search_knowledge(
    project_id: uuid.UUID,
    data: RetrievalRequest,
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

    count = db.scalar(
        select(
            func.count(
                KnowledgeChunk.id
            )
        ).where(
            KnowledgeChunk.project_id
            == project_id
        )
    )

    if not count:

        raise HTTPException(
            status_code=400,
            detail=(
                "Project knowledge index "
                "has not been built"
            ),
        )

    results = retrieve_project_evidence(
        project_id=project_id,
        query=data.query,
        top_k=data.top_k,
        evidence_types=
            data.evidence_types,
    )

    return {
        "query": data.query,
        "results": results,
    }
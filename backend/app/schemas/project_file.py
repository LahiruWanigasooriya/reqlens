import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectFileResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID

    original_name: str
    file_type: str
    mime_type: str | None

    size_bytes: int

    processing_status: str
    processing_error: str | None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
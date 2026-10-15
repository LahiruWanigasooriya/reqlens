import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    requirement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "requirements.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    criterion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "verifiable_criteria.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    project_file_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "project_files.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    vector_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    source_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    evidence_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    relevance_score: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    semantic_score: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    strength: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    supports_criterion: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    explanation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    extracted_fact: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
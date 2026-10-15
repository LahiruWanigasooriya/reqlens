import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserStory(Base):
    __tablename__ = "user_stories"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "external_id",
            name="uq_story_project_external_id",
        ),
    )

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

    source_file_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "project_files.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    requirement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "requirements.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    external_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    issue_type: Mapped[str] = mapped_column(
        String(100),
        default="Story",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AcceptanceCriterion(Base):
    __tablename__ = "acceptance_criteria"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    story_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "user_stories.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    criterion_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
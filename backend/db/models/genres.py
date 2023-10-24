from .base import Base

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Genre(Base):
    __tablename__ = "genres"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(
        String,
        nullable=False,
        unique=True
    )

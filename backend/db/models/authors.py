from .base import Base

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Author(Base):
    __tablename__ = "authors"

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

    # books relationship
    books = relationship(
        "BookAuthor",
        back_populates="author"
    )

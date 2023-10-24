from .base import Base

from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Book(Base):

    __tablename__ = "books"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title = Column(
        String,
        nullable=False,
        unique=True
    )

    # foreign keys
    genre_id = Column(
        UUID(as_uuid=True),
        ForeignKey("genres.id")
    )

    # authors relationship
    authors = relationship(
        "BookAuthor",
        back_populates="book"
    )

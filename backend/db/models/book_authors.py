from .base import Base

from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy

import uuid


class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("books.id"),
        primary_key=True,
    )
    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("authors.id"),
        primary_key=True
    )
    book = relationship("Book", back_populates="authors")
    author = relationship("Author", back_populates="books")

    author_name = association_proxy(target_collection='author', attr='name')
    book_title = association_proxy(target_collection='book', attr='title')

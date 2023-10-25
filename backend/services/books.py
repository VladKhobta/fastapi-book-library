from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, List

from schemas.books import BookCreation, BookShowing, BookUpdate
from db.session import get_session
from db.dals import BookDAL, AuthorDAL, GenreDAL

from uuid import UUID


class BookService:

    def __init__(
            self,
            session: AsyncSession = Depends(get_session)
    ):
        self.session = session

    async def create(
            self,
            body: BookCreation,
    ) -> UUID:
        authors = []
        author_dal = AuthorDAL(self.session)
        for name in body.authors:
            authors.append(await author_dal.get_by_name(name))
        genre_dal = GenreDAL(self.session)
        genre = await genre_dal.get_by_name(body.genre)
        book_dal = BookDAL(self.session)
        new_book = await book_dal.create(
            title=body.title,
            genre=genre,
            authors=authors
        )
        return new_book.id

    async def get_by_id(
            self,
            book_id: UUID
    ) -> Union[BookShowing, None]:
        book_dal = BookDAL(self.session)
        book = await book_dal.get_by_id(book_id)

        if not book:
            return None

        author_dal = AuthorDAL(self.session)
        authors = []
        for book_author in book.authors:
            author = await author_dal.get_by_id(book_author.author_id)
            authors.append(author.name)
        if book:
            return BookShowing(
                title=book.title,
                authors=authors,
                genre_id=book.genre_id
            )

    async def get_by_title(
            self,
            book_title: str
    ) -> Union[BookShowing, None]:
        book_dal = BookDAL(self.session)
        book = await book_dal.get_by_title(book_title)

        if not book:
            return None

        author_dal = AuthorDAL(self.session)
        authors = []
        for book_author in book.authors:
            author = await author_dal.get_by_id(book_author.author_id)
            authors.append(author.name)
        if book:
            return BookShowing(
                title=book.title,
                authors=authors,
                genre_id=book.genre_id
            )

    async def get_all(
            self,
            skip: int,
            limit: int
    ) -> List[str]:
        book_dal = BookDAL(self.session)
        books = await book_dal.get_all(skip, limit)
        return [book.title for book in books]

    async def delete(
            self,
            book_id: UUID
    ) -> UUID:
        book_dal = BookDAL(self.session)
        return await book_dal.delete(book_id)

    async def update(
            self,
            book_id: UUID,
            body: BookUpdate
    ) -> UUID:
        authors = []
        author_dal = AuthorDAL(self.session)
        for name in body.authors:
            authors.append(await author_dal.get_by_name(name))
        genre_dal = GenreDAL(self.session)
        genre = await genre_dal.get_by_name(body.genre)
        book_dal = BookDAL(self.session)

        await book_dal.delete(book_id)
        new_book = await book_dal.create(
            title=body.title,
            authors=authors,
            genre=genre
        )
        return new_book.id

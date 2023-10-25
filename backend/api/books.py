from fastapi import APIRouter, Depends, HTTPException, Query

from uuid import UUID
from typing import List, Union

from schemas.books import BookCreation, BookShowing
from services import BookService, AuthorService, GenreService

book_router = APIRouter()


@book_router.get("/")
async def get_books(
        skip: int = Query(default=0, description="Number of books to skip"),
        limit: int = Query(default=30, description="Number of books to return"),
        book_title: str = Query(default=None, title="Book title"),
        book_service: BookService = Depends()
) -> Union[List[str], BookShowing]:
    if book_title:
        book_showing = await book_service.get_by_title(book_title)
        if not book_showing:
            raise HTTPException(
                status_code=404,
                detail=f"Book with {book_title} title is not found"
            )
        return book_showing
    return await book_service.get_all(skip, limit)


@book_router.get("/{book_id}")
async def get_book_by_id(
        book_id: UUID,
        book_service: BookService = Depends()
) -> BookShowing:
    book = await book_service.get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Book with {book_id} id is not found"
        )
    return book


@book_router.post("/")
async def create_book(
        body: BookCreation,
        book_service: BookService = Depends(),
        author_service: AuthorService = Depends(),
        genre_service: GenreService = Depends()
) -> UUID:
    for name in body.authors:
        if not await author_service.get_by_name(name):
            raise HTTPException(
                status_code=404,
                detail=f"Author with {name} name is not found"
            )
    if body.genre and not await genre_service.get_by_name(body.genre):
        raise HTTPException(
            status_code=404,
            detail=f"{body.genre} genre is not found"
        )
    if await book_service.get_by_title(body.title):
        raise HTTPException(
            status_code=409,
            detail=f"Book with {body.title} title is already exists"
        )
    return await book_service.create(body)


@book_router.delete("/{book_id}")
async def delete_book(
        book_id: UUID,
        book_service: BookService = Depends()
) -> UUID:
    if not await book_service.get_by_id(book_id):
        raise HTTPException(
            status_code=404,
            detail=f"Book with {book_id} id is not found"
        )
    return await book_service.delete(book_id)


@book_router.put("/{book_id}")
async def update_book(
        book_id: UUID,
        body: BookCreation,
        book_service: BookService = Depends(),
        author_service: AuthorService = Depends(),
        genre_service: GenreService = Depends()
) -> UUID:
    if not await book_service.get_by_id(book_id):
        raise HTTPException(
            status_code=404,
            detail=f"Book with {book_id} id is not found"
        )
    for name in body.authors:
        if not await author_service.get_by_name(name):
            raise HTTPException(
                status_code=404,
                detail=f"Author with {name} name is not found"
            )
    if body.genre and not await genre_service.get_by_name(body.genre):
        raise HTTPException(
            status_code=404,
            detail=f"{body.genre} genre is not found"
        )
    return await book_service.update(book_id, body)

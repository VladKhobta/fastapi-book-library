from fastapi import APIRouter, Depends, HTTPException

from typing import List
from uuid import UUID

from schemas.authors import AuthorShowing, AuthorCreation, AuthorUpdate
from services import AuthorService



author_router = APIRouter()


@author_router.get("/")
async def get_authors(
        author_service: AuthorService = Depends()
) -> List[AuthorShowing]:
    return await author_service.get_all()


@author_router.get("/{author_id}")
async def get_author_by_id(
        author_id: UUID,
        author_service: AuthorService = Depends()
) -> AuthorShowing:
    author = await author_service.get_by_id(author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"Author with {author_id} id is not found"
        )
    return author


@author_router.post("/")
async def create_author(
        body: AuthorCreation,
        author_service: AuthorService = Depends()
) -> UUID:
    if await author_service.get_by_name(body.name):
        raise HTTPException(
            status_code=409,
            detail=f"Author with {body.name} name is already exists"
        )
    return await author_service.create(body)


@author_router.delete("/{book_id}")
def delete_author(
        book_id: UUID
):
    pass


@author_router.put("/{author_id}")
async def update_author(
        author_id: UUID,
        body: AuthorUpdate,
        author_service: AuthorService = Depends()
) -> AuthorShowing:
    if not await author_service.get_by_id(author_id):
        raise HTTPException(
            status_code=404,
            detail=f"Author with {author_id} id is not found"
        )
    updated_recipient_data = body.model_dump(exclude_none=True)
    return await author_service.update(
        author_id, updated_recipient_data
    )

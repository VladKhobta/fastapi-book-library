from fastapi import APIRouter, Depends, HTTPException

from uuid import UUID
from typing import List

from schemas.genres import GenreCreation, GenreShowing
from services import GenreService


genre_router = APIRouter()


@genre_router.get("/")
async def get_genres(
        genre_service: GenreService = Depends()
) -> List[GenreShowing]:
    return await genre_service.get_all()


@genre_router.post("/")
async def create_genre(
        body: GenreCreation,
        genre_service: GenreService = Depends()
) -> UUID:
    if await genre_service.get_by_name(body.name):
        raise HTTPException(
            status_code=409,
            detail=f"{body.name} genre is already exists"
        )
    return await genre_service.create(body)

import uvicorn

from fastapi import FastAPI, APIRouter

from api.books import book_router
from api.authors import author_router
from api.genres import genre_router

app = FastAPI(
    title="FastAPI book library",
)

main_api_router = APIRouter()

main_api_router.include_router(
    book_router,
    prefix="/books",
    tags=["books"]
)
main_api_router.include_router(
    author_router,
    prefix="/authors",
    tags=["authors"]
)
main_api_router.include_router(
    genre_router,
    prefix="/genres",
    tags=["genres"]
)

app.include_router(
    main_api_router,
    prefix="/api"
)



if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8888,
    )

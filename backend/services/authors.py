from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID
from typing import Union, List

from schemas.authors import AuthorCreation, AuthorShowing
from db.session import get_session
from db.dals import AuthorDAL


class AuthorService:

    def __init__(
            self,
            session: AsyncSession = Depends(get_session)
    ):
        self.session = session

    async def create(
            self,
            body: AuthorCreation,
    ) -> UUID:
        author_dal = AuthorDAL(self.session)
        new_author = await author_dal.create(
            name=body.name
        )
        return new_author.id

    async def get_by_id(
            self,
            author_id: UUID
    ) -> AuthorShowing:
        author_dal = AuthorDAL(self.session)
        author = await author_dal.get_by_id(author_id)
        if author:
            return AuthorShowing(name=author.name)

    async def get_by_name(
            self,
            name: str
    ) -> Union[AuthorShowing, None]:
        author_dal = AuthorDAL(self.session)
        author = await author_dal.get_by_name(name)
        if author:
            return AuthorShowing(name=author.name)

    async def get_all(self) -> List[AuthorShowing]:
        author_dal = AuthorDAL(self.session)
        authors = await author_dal.get_all()
        return [AuthorShowing(name=author.name) for author in authors]

    async def update(
            self,
            author_id: UUID,
            author_updated_data: dict
    ) -> Union[AuthorShowing, None]:
        author_dal = AuthorDAL(self.session)
        updated_author = await author_dal.update(author_id, **author_updated_data)
        if updated_author:
            return AuthorShowing(
                name=updated_author.name
            )

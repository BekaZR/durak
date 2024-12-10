from typing import AsyncGenerator, Callable, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core.lifespan import session_factory
from db.crud.base import BaseCRUD


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()


async def get_db_session_ws() -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param None
    :yield: database session.
    """
    session: AsyncSession = session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()


def get_dao(dao: Type[BaseCRUD]) -> Callable[[AsyncSession], BaseCRUD]:
    def _get_repo(
        session: AsyncSession = Depends(get_db_session_ws),
    ) -> BaseCRUD:
        return dao(session)

    return _get_repo

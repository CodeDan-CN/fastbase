from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from config.db_config import async_session


async def get_session():
    async with async_session() as session:
        yield session

def with_session(func):
    async def wrapper(*args, session: AsyncSession = Depends(get_session), **kwargs):
        return await func(*args, session=session, **kwargs)
    return wrapper


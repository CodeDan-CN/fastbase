import os

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./db_file/test.db"  # 当前目录下的 test.db 文件

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# 可选：首次启动建表用
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

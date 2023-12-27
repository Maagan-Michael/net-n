from sqlalchemy import exc
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from ..config import AppConfig
# using sqlite in dev environment, but will change to postgresql in production
### dev environment only ###
Base = declarative_base()


def getDBUrl() -> str:
    return f"postgresql+asyncpg://{AppConfig['db']['user']}:{AppConfig['db']['password']}@{AppConfig['db']['host']}:{AppConfig['db']['port']}/{AppConfig['db']['database']}"


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """get database session"""
    url = getDBUrl()
    engine = create_async_engine(url)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


get_context_db_session = asynccontextmanager(get_db_session)


async def create_db() -> None:
    """create database utility"""
    url = getDBUrl()
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """drop database utility"""
    url = getDBUrl()
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# deprecated

# automaped (for sql sync module) : get the schema from the database and map it to the classes
# AutoMapBase = automap_base()
# @asynccontextmanager
# async def get_context_mapped_db_session():
#     """get database session"""
#     url = getDBUrl()
#     engine = create_async_engine(url)
#     factory = async_sessionmaker(engine)
#     async with factory() as session:
#         AutoMapBase = automap_base()
#         AutoMapBase.prepare(engine, reflect=True)
#         try:
#             yield session, AutoMapBase.classes
#             await session.commit()
#         except exc.SQLAlchemyError as e:
#             await session.rollback()
#             raise e
#         finally:
#             await session.close()

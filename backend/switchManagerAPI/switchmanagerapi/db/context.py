from sqlalchemy import exc
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

# using sqlite in dev environment, but will change to postgresql in production
### dev environment only ###
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:password@0.0.0.0:5432/postgres"
Base = declarative_base()


async def get_db_session(url: str = SQLALCHEMY_DATABASE_URL) -> AsyncGenerator[AsyncSession, None]:
    """get database session"""
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


@asynccontextmanager
async def get_context_db_session(url: str = SQLALCHEMY_DATABASE_URL):
    """get database session"""
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


async def create_db() -> None:
    """create database"""
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """drop database"""
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# automaped (for sql sync module)

AutoMapBase = automap_base()


@asynccontextmanager
async def get_context_mapped_db_session(url: str = SQLALCHEMY_DATABASE_URL):
    """get database session"""
    engine = create_async_engine(url)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        AutoMapBase = automap_base()
        AutoMapBase.prepare(engine, reflect=True)
        try:
            yield session, AutoMapBase.classes
            await session.commit()
        except exc.SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

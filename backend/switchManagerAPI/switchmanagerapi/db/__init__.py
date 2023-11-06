from sqlalchemy import exc
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

# using sqlite in dev environment, but will change to postgresql in production
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
Base = declarative_base()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """get database session"""
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
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
async def get_context_db_session():
    """get database session"""
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
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

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# using sqlite in dev environment, but will change to postgresql in production
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db_session():
    """get database session"""
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except exc.SQLAlchemyError as e:
        await session.rollback()
        raise e
    finally:
        session.close()


def create_db():
    """create database"""
    Base.metadata.create_all(bind=engine)

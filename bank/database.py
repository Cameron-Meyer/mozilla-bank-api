import os

from pydantic import BaseSettings
from sqlalchemy import create_engine, Column, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support
class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = f"envs/{os.getenv('RUNTIME_ENV', 'dev')}.env"


engine = create_engine(Settings().database_url)
Base = declarative_base()
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Initializes the database and manages its connection, closing on completion

    :return: the DB Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Account(Base):
    __tablename__ = "accounts"

    name = Column(String, primary_key=True, index=True, unique=True)
    balance = Column(Numeric, default=0.00)

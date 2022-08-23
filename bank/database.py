from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Settings

engine = create_engine(Settings().database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


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

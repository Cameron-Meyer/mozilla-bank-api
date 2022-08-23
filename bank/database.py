from sqlalchemy import create_engine, Column, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Settings

engine = create_engine(Settings().database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"

    name = Column(String, primary_key=True, index=True, unique=True)
    balance = Column(Numeric, default=0.00)

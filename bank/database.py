from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Would normally externalize to allow for using local container vs independent, distributed container,
# but for the purposes of this exercise this is fine
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mozilla@bank-db/Bank"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

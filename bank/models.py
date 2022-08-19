from sqlalchemy import Column, String, Numeric

from .database import Base


class Account(Base):
    __tablename__ = "Accounts"

    name = Column(String, primary_key=True, index=True)
    amount = Column(Numeric)

from sqlalchemy import Column, String, Numeric

from database import Base


class Account(Base):
    __tablename__ = "accounts"

    name = Column(String, primary_key=True, index=True, unique=True)
    balance = Column(Numeric, default=0.00)

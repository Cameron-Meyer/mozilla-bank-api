from sqlalchemy.orm import Session
from . import models, schemas


def create_account(db: Session, name: str):
    new_account = models.Account(name=name)
    # return db.

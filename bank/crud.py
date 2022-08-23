from decimal import Decimal

from sqlalchemy.orm import Session

from models import Account
import schemas


def get_account(db: Session, account_name: str):
    """
    Locates the account by the provided name. Returns only one result

    :param db: Connection to execute the queries on
    :param account_name: to filter on
    :return: schemas.Account
    :raise sqlalchemy.exc.NoResultFound: if no record is returned
    """
    return db.query(Account).filter_by(name=account_name).one()


def create_account(db: Session, account: schemas.Account):
    """
    Creates a new account with the given name; if no amount is provided, it will default to 0.0
    :param db: Connection to execute on
    :param account: Name, and optionally amount, to add
    :return: the account as stored in the DB
    :raise sqlalchemy.exc.IntegrityError: if an account already exists with the name provided
    """
    # Ordinarily would make case-insensitive, but given lack of requirements I'll default to "Case Matters"
    new_account = Account(name=account.name)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


def update_amount(db: Session, account: schemas.Account):
    # Provides two benefits: Validates that only one account exists, and loads the object into session so that
    # synchronize_session updates it upon completion (ensuring we get the most up-to-date record
    updated_account = get_account(db, account.name)
    db.query(Account).filter_by(name=account.name).update(
        {Account.balance: updated_account.balance + Decimal(account.balance)},
        synchronize_session='fetch')
    db.commit()
    return updated_account

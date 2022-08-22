from sqlalchemy.orm import Session
import models, schemas


def get_account(db: Session, account_name: str):
    """
    Locates the account by the provided name. Returns only one result

    :param db: Connection to execute the queries on
    :param account_name: to filter on
    :return: schemas.Account
    :raise sqlalchemy.exc.NoResultFound: if no record is returned
    """
    return db.query(models.Account).filter_by(name=account_name).one()


def create_account(db: Session, account: schemas.Account):
    """
    Creates a new account with the given name; if no amount is provided, it will default to 0.0
    :param db: Connection to execute on
    :param account: Name, and optionally amount, to add
    :return: the account as stored in the DB
    :raise sqlalchemy.exc.IntegrityError: if an account already exists with the name provided
    """
    new_account = models.Account(name=account.name)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


def deposit_amount(db: Session, account: schemas.Account):
    # Provides two benefits: Validates that only one account exists, and loads the object into session so that
    # synchronize_session updates it upon completion (ensuring we get the most up-to-date record
    updated_account = get_account(db, account.name)
    db.query(models.Account).filter_by(name=account.name).update({models.Account.amount: account.amount},
                                                                 synchronize_session='fetch')
    db.commit()
    return updated_account

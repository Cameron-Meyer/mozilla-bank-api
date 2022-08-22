from fastapi import FastAPI, Depends, HTTPException, Request, Path, Body
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.exception_handler(NoResultFound)
async def no_result_handler(request: Request, exc: NoResultFound):
    return JSONResponse(status_code=404, content=None)


@app.post("/account", response_model=schemas.Account, status_code=201)
async def create_account(account: schemas.Account, db: Session = Depends(get_db)):
    try:
        return crud.create_account(db, schemas.Account(name=account.name))
    except IntegrityError:
        raise HTTPException(status_code=409, detail="The provided account already exists")


@app.get("/account/{name}", response_model=schemas.Account)
async def retrieve_account(name: str, db: Session = Depends(get_db)):
    return crud.get_account(db, name)


@app.post("/account/{name}/deposit", response_model=schemas.Account, status_code=201)
async def deposit_amount(name: str = Path(title="Name of the account to deposit the amount under"),
                         amount: float = Body(title="Amount greater than 0 to deposit to the specified account",
                                              gt=0,
                                              embed=True),
                         db: Session = Depends(get_db)):
    return crud.deposit_amount(db, schemas.Account(name=name, amount=amount))

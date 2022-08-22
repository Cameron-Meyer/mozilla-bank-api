import urllib.parse

from fastapi import FastAPI, Depends, HTTPException, Request, Path, Body, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank API - Mozilla Take-Home Assessment", contact={"Cameron Meyer": "c.meyer95@gmail.com"})


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


responses = {
    404: {"description": "Account was not found", "content": {}},
}


@app.post("/account",
          response_model=schemas.Account,
          status_code=201,
          responses={201: {"description": "Account creation succeeded",
                           # https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#link-object
                           "links": {"Location": {"operationId": "retrieve_account_account__name__get",
                                                  "parameters": {"name": "$request.body.name"}}
                                     }},
                     409: {"description": "The provided account already exists",
                           "content": {
                               "application/json": {"example": {"detail": "The provided account already exists"}}
                           }}
                     }
          )
async def create_account(response: Response, account: schemas.Account, db: Session = Depends(get_db)):
    try:
        account = crud.create_account(db, schemas.Account(**account.dict()))
        # https://restfulapi.net/http-status-201-created/
        response.headers["Location"] = urllib.parse.quote(f"/account/{account.name}")
        return account
    except IntegrityError:
        raise HTTPException(status_code=409, detail="The provided account already exists")


@app.get("/account/{name}", response_model=schemas.Account, responses={**responses})
async def retrieve_account(name: str, db: Session = Depends(get_db)):
    return crud.get_account(db, name)


@app.post("/account/{name}/deposit", response_model=schemas.Account, responses={**responses})
async def deposit_amount(name: str = Path(title="Name of the account to deposit the amount under"),
                         amount: float = Body(title="Amount greater than 0 to deposit to the specified account",
                                              gt=0,
                                              embed=True),
                         db: Session = Depends(get_db)):
    return crud.update_amount(db, schemas.Account(name=name, amount=amount))


@app.post("/account/{name}/withdraw", response_model=schemas.Account, responses={**responses})
async def withdraw_amount(name: str = Path(title="Name of the account to withdraw the amount from"),
                          amount: float = Body(title="Amount greater than 0 to withdraw from the specified account",
                                               gt=0,
                                               embed=True),
                          db: Session = Depends(get_db)):
    return crud.update_amount(db, schemas.Account(name=name, amount=amount * -1))

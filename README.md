# Mozilla Take-home Exercise: Bank API

## Requirements - [Original PDF](./instructions.pdf)

### API Requirements
- POST `/account`
  - Create an account with the given name and a balance of 0.00.
  - Request Body: `{"name": "#string"}` 

- GET `/account/:name`
  - Retrieve an account by its name. If an account with the given name does not exist, return HTTP status 404
with no response body.
  - Response Body: `{ "name": "#string", "balance": #float }`

- POST `/account/:name/deposit`
  - Deposit money into the account with the given name. If an account with the given name does not exist,
return HTTP status 404 with no response body.
  - Request Body Format: `{ "amount": #float }`

- POST `/account/:name/withdraw`
  - Withdraw money from the account with the given name. If an account with the given name does not exist,
return HTTP status 404 with no response body.
  - Request Body Format: `{ "amount": #float }`

## Approach
### Design
Not much to layout here, instructions were explicit and well-documented. I did add some additional behavior based on common standards for REST APIs:
- Application-wide
  - 400 if `name` doesn't contain non-special characters + whitespace 
- `POST /account`
  - Returning a `Location` header on 201
  - 409 for conflicting primary keys (account name)
- `POST /deposit` + `POST /withdraw`
  - 400 if `amount` is not in `#.##` or `#` format

### Build Tool - [Poetry](https://python-poetry.org/)
Primarily because I saw it being used in https://github.com/mozilla-services/merino-py (fya, there's a typo of `[Follow the] insturctions` in the readme, under Setup), so its likely familiarity with reviewers 
and its approach to packaging dependencies (which was familiar to me thanks to my experience with Gradle, Maven, and NPM) made it an easy choice for this task.

### Primary Framework - [FastApi](https://fastapi.tiangolo.com/)
Primarily chosen due to being, well, fast to develop. My Python isn't nearly as strong as my Java currently, so I specifically wanted
a framework that was concise and easy to pick up, but still powerful and familiar to experienced Python devs. Light research mentioned this framework
in several sources as a strong up-and-comer in the industry, and its concise, type-hint heavy syntax felt familiar enough to me that I felt I could 
focus more on the given task rather than on learning an entire new framework in a moderately unfamiliar language for a one-off task 
(understanding that the actual job will use similar concepts, but in an established codebase with a significantly different set of requirements and interactions).  

### Supporting Libaries
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM Library
  - One of the options recommended by https://fastapi.tiangolo.com/tutorial/sql-databases/ - chosen for compatibility with documentation and its independence of framework 
      (personal preference is to prioritize reusability of business logic regardless of framework, unless there are significant benefits to native integration)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
  - Paired with SQLAlchemy to perform Schema validation
- [Uvicorn](https://www.uvicorn.org/) - Local ASGI Web Server
  - Comes packaged with FastAPI, used in many examples online, extremely lightweight and quick to set up


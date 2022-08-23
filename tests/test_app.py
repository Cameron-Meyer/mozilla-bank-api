# https://fastapi.tiangolo.com/advanced/testing-database/

from fastapi.testclient import TestClient

import bank.main

client = TestClient(bank.main.app)


# Wanted to do integrationTests, but can't get SQLAlchemy to create the tables on the same instance of the engine
# as is being used by main and crud. Tried multiple ways of organizing and calling, including and based off of
# https://fastapi.tiangolo.com/tutorial/sql-databases/#review-all-the-files, but no luck.


# def test_create_account():
#     response = client.post(
#         "/account",
#         json={"name": "Testing McTest"},
#     )
#     assert response.status_code == 201, response.text
#     data = response.json()
#     assert data["name"] == "Testing McTest"
#     assert data["balance"] == 0
#
#     name = data["name"]
#     response = client.get(f"/account/{name}")
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["email"] == name
#     assert data["balance"] == 0

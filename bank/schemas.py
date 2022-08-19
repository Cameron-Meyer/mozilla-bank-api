import re
from typing import Optional

from pydantic import BaseModel, validator


class Account(BaseModel):
    name: str
    amount: Optional[float]

    @validator('name', always=True, pre=True)
    def name_must_be_alpha_and_spaces(cls, name: str):
        if not name or not name.strip():
            # Pydantic will prepend error message with '1 validation error for Account\nname\n'
            raise ValueError("field required, but is either empty or pure whitespace")
        elif not re.match('^[a-zA-Z\\s]+$', name):
            raise ValueError("field contains non-alpha and non-whitespace characters")

        return name

    class Config:
        orm_mode = True

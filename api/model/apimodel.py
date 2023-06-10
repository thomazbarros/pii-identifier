from typing import Union
from pydantic import BaseModel


class APIModel(BaseModel):
    host: str
    port: Union[int, None] = 3306
    username: str
    password: Union[str, None] = None

    class Config:
        orm_mode = True
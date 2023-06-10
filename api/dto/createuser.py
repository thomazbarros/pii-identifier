from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    name: str
    username: str
    password: str
from pydantic import BaseModel

class UserDTO(BaseModel):
    id: int | None
    name: str | None
    username: str | None
    password: str | None
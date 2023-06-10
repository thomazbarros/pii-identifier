from pydantic import BaseModel

class RuleDTO(BaseModel):
    name: str | None
    regex_exp: str | None
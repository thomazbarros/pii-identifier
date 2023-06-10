from fastapi import APIRouter, Header, status, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from dto.login import LoginDTO
import jwt

from service.user import UserService
from service.token import TokenService

user_service = UserService()
token_service = TokenService()

router = APIRouter(
    prefix="/api/v1/login",
    tags=["login"]
)

@router.post("/", status_code=status.HTTP_200_OK, description="Log user into application. Returns a JWT token to be used into private routers.")
def login(dto: LoginDTO):
    try: 
        user_service.login(dto.username, dto.password)
        token = token_service.create_jwt_token(dto.username)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Username or password are incorrect"})


async def get_token_header(x_token: Annotated[str, Header()]):
    try:
        payload = token_service.decode(x_token)
        users = user_service.find(username=payload.get("sub"))
        if users.count == 0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
from fastapi import APIRouter, Depends,  Request, Query, HTTPException, status
from routers.public.login import get_token_header
from service.user import UserService
from dto.createuser import CreateUserDTO
from exception.entityalreadyexistsexception import EntityAlreadyExistsException

async def skip():
    return None

user_service = UserService()
router = APIRouter(
    prefix="/api/v1/user",
    tags=["user"],
)

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create a new user", dependencies=None)
async def create_user(dto: CreateUserDTO):
    try:
        id = user_service.create_user(name = dto.name, username = dto.username, password = dto.password)
        return {"id": id}
    except EntityAlreadyExistsException:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="User with username " + dto.username + " already exists")
    except Exception as ex:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error. Reason:" + str(ex.args))

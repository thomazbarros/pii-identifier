from fastapi import APIRouter, Depends, Response, Query, status
from routers.public.login import get_token_header
from service.user import UserService
async def skip():
    return None

user_service = UserService()
router = APIRouter(
    prefix="/api/v1/user",
    tags=["user"],
    dependencies=[Depends(get_token_header)],
)

@router.get("/", status_code=status.HTTP_200_OK, summary='Get a list of all users')
async def get_users(name: str = Query(default=None, title="User's name", description='Search users by name')):
    return user_service.find(name)

@router.get("/{userId}", status_code=status.HTTP_200_OK, summary="Return a user given an id")
async def get_user(userId, response: Response,):
    user = user_service.get_user_by_id(userId)
    if user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "User not found."}
    return user


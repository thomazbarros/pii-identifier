from fastapi import Depends, APIRouter, status

router = APIRouter(
    prefix="/healthcheck",
    tags=["monitoring"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=status.HTTP_200_OK)
async def healthcheck():
    return "I'm alive."


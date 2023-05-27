from fastapi import APIRouter, Depends
from controller.auth_controller import get_current_user

router = APIRouter()

@router.get("/")
async def hello(token: str = Depends(get_current_user)):
    return {"message":"hello world"}
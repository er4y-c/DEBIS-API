from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def hello():
    return {"message":"hello world"}
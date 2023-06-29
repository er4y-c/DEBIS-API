from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from db.database import Session, engine
from controller.auth_controller import get_current_user
from crud.announcement import get_all_announcement

router = APIRouter()
session = Session(bind=engine)

@router.get("/")
def get_all_announce(user = Depends(get_current_user)):
    data = get_all_announcement()

    try:
        return JSONResponse(
            status_code=200,
            content={
                "announcements": jsonable_encoder(data)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"An error occurred. Error details: {str(e)}"
            }
        )

@router.post("/create")
def create_announcement(user = Depends(get_current_user)):
    pass
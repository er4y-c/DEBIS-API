from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from db.database import Session, engine
from datetime import datetime
from controller.auth_controller import get_current_user
from crud.announcement import get_all_announcement, add_announcement, get_announcement_by_lesson
from schemas.announcement_schema import AnnouncementModel
from models.models import Announcement
from controller.lesson_controller import get_lesson_by_code

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

@router.get("/get_lesson_announcement")
def get_all_announce(lesson_code: str, user = Depends(get_current_user)):
    current_lesson = get_lesson_by_code(lesson_code) 
    data = get_announcement_by_lesson(current_lesson.id)
    if len(data) <= 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Announcements not found"
            }
        )
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
def create_announcement(announcement: AnnouncementModel, user = Depends(get_current_user)):
    current_lesson = get_lesson_by_code(announcement.lesson_code)
    current_date = datetime.now()
    new_announce = Announcement(
        lesson_id = current_lesson.id,
        announcement_title = announcement.title,
        announcement_content = announcement.content,
        announcement_date = current_date
    )
    
    try:
        add_announcement(new_announce)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Announcement add successfully"
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"An error occurred. Error details: {str(e)}"
            }
        )
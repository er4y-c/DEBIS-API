from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from controller.auth_controller import get_current_user
from schemas.lesson_schema import AddLessonModel
from models.models import Lesson, Teacher
from controller.auth_controller import authenticate_token
from db.database import Session, engine
from fastapi.encoders import jsonable_encoder
router = APIRouter()
session = Session(bind=engine)

@router.get("/")
async def hello(user: str = Depends(get_current_user)):
    return {"message":"hello world"}

@router.post("/create")
async def create_lesson(lesson: AddLessonModel, user: str = Depends(get_current_user)):
    exist_lesson = session.query(Lesson).filter(Lesson.lesson_code==lesson.lesson_code or Lesson.lesson_name==lesson.lesson_name).first()
    
    if exist_lesson:
        raise HTTPException(
            status_code=409,
            detail="This course already exist"
        )
    
    try:
        teacher = session.query(Teacher).filter(user.email == Teacher.email).first()
    except Exception as e:
         return JSONResponse(
            status_code=500,
            content= {
                "message": f"Error detail: {str(e)}"
            }
        )
    if not teacher:
        return JSONResponse(
            status_code=401,
            content= {
                "message": "No authorization for this process"
            }
        )
    try:
        new_lesson = Lesson(
            lesson_code = lesson.lesson_code,
            lesson_name = lesson.lesson_name,
            teacher_id = teacher.id,
            lesson_credit = lesson.lesson_credit,
            lesson_department = lesson.lesson_department
        )

        session.add(new_lesson)
        session.commit()

        return JSONResponse(
                status_code=200,
                content={
                    "message":"Course is created succesfully",
                },
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred. Error details: {str(e)}"
        )
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from controller.auth_controller import get_current_user
from schemas.lesson_schema import AddLessonModel, AddStudentLessonModel, AddNoteModel
from models.models import Lesson, Teacher
from db.database import Session, engine
from crud.lesson import get_lesson_by_code, get_lesson_by_id
from controller.lesson_controller import create_id_list, assign_lesson_controller, add_notes_controller

router = APIRouter()
session = Session(bind=engine)

@router.get("/")
async def get_lessons(user: str = Depends(get_current_user)):
    try:
        lessons = get_lessons()
        return JSONResponse(
            status_code=200,
            content={
                "course_list": jsonable_encoder(lessons)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"An error occurred. Error details: {str(e)}"
            }
        )
    
@router.get("/{lesson_id}")
async def get_lesson(lesson_id: int, user: str = Depends(get_current_user)):
    try:
        lesson = get_lesson_by_id(lesson_id)
        return JSONResponse(
            status_code=200,
            content={
                "course_detail": jsonable_encoder(lesson)
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

@router.post("/assign-student")
async def assign_lesson_to_student(lesson: AddStudentLessonModel, user: str = Depends(get_current_user)):
    find_lesson = get_lesson_by_code(lesson.lesson_code)
    if not find_lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson is not found"
        )
    try:
        student_id_list = create_id_list(lesson.student_list)

        new_student_lesson = assign_lesson_controller(student_id_list, find_lesson.id)
        session.add(new_student_lesson)
        session.commit()

        return JSONResponse(
            status_code=200,
            content={
                "message": "Students added successfully"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred. Error details: {str(e)}"},
        )

@router.put("/add_note")
async def add_note(note_data: AddNoteModel, user: str = Depends(get_current_user)):
    try:
        add_notes_controller(note_data)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Notes added successfully"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred. Error details: {str(e)}"},
        )

@router.post("/assign-teacher")
async def assign_lesson_to_teacher(lesson: AddLessonModel, user: str = Depends(get_current_user)):
    pass
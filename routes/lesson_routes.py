from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Union
from controller.auth_controller import get_current_user
from schemas.auth_schema import SignUpStudentModel, SignUpTeacherModel
from schemas.lesson_schema import AddLessonModel, AddStudentLessonModel, AddNoteModel
from models.models import Lesson, Teacher, TeacherLesson
from db.database import Session, engine
from crud.lesson import get_lesson_by_code, get_lesson_by_id, add_lesson, add_teacher_lesson, get_student_all_lesson, get_current_semester
from controller.lesson_controller import create_id_list, assign_lesson_controller, add_notes_controller, assign_teacher_controller

router = APIRouter()
session = Session(bind=engine)

@router.get("/")
async def get_lessons(user = Depends(get_current_user)):
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
async def get_lesson(lesson_id: int, user = Depends(get_current_user)):
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
    
@router.get("/student_all_lesson/{student_id}")
async def get_student_lessons(student_id: int, user = Depends(get_current_user)):
    try:
        lessons = get_student_all_lesson(student_id)
            
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

@router.get("/student_semester_lesson/{student_id}")
async def get_student_lessons(student_id: int, year: int, semester: int, user = Depends(get_current_user)):
    
    try:
        lesson_codes = []
        lesson_names = []
        lessons = get_current_semester(student_id, year, semester)
        for lesson in lessons:
            temp = get_lesson_by_id(lesson.lesson_id)
            lesson_codes.append(temp.lesson_code)
            lesson_names.append(temp.lesson_name)

        return JSONResponse(
            status_code=200,
            content={
                "course_list": jsonable_encoder(lessons),
                "course_codes": jsonable_encoder(lesson_codes),
                "course_names": jsonable_encoder(lesson_names)
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
async def create_lesson(lesson: AddLessonModel, user = Depends(get_current_user)):
    exist_lesson = session.query(Lesson).filter(Lesson.lesson_code==lesson.lesson_code or Lesson.lesson_name==lesson.lesson_name).first()
    
    if exist_lesson:
        raise HTTPException(
            status_code=409,
            detail="This course already exist"
        )

    teacher = session.query(Teacher).filter(user.email == Teacher.email).first()
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
        add_lesson(new_lesson)

        current_lesson = get_lesson_by_code(lesson.lesson_code)
        new_lesson_teacher = TeacherLesson(
            lesson_id = current_lesson.id,
            teacher_id = teacher.id
        )
        add_teacher_lesson(new_lesson_teacher)

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
async def assign_lesson_to_student(lesson: AddStudentLessonModel, user = Depends(get_current_user)):
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
async def add_note(note_data: AddNoteModel, user = Depends(get_current_user)):
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

@router.put("/assign-teacher")
async def assign_lesson_to_teacher(lesson_code: str, teacher_id: int, user = Depends(get_current_user)):
    try:
        temp = assign_teacher_controller(lesson_code, teacher_id)
        if temp:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Assignment done succesfully"
                }
            )
        return JSONResponse(
            status_code=500,
            content={"message": "Lesson did not assign to teacher"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred. Error details: {str(e)}"},
        )
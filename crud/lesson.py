from db.database import Session, engine
from models.models import Lesson, StudentLesson, TeacherLesson
from sqlalchemy import update, select
from sqlalchemy.sql import distinct

session = Session(bind=engine)

def get_lesson_by_code(lesson_code):
    return session.query(Lesson).filter(lesson_code == Lesson.lesson_code).first()

def get_lessons():
    return session.query(Lesson).all()

def get_lesson_by_id(lesson_id):
    return session.query(Lesson).filter(Lesson.id == lesson_id).first()

def update_notes(student_id, lesson_id, ara_sinav, final, diger_sinav):
    
    temp = update(StudentLesson).where(StudentLesson.student_id == student_id and StudentLesson.lesson_id == lesson_id).values(ara_sinav=ara_sinav, final=final, diger_sinav=diger_sinav)
    session.execute(temp)
    session.commit()

def add_lesson(lesson):
    session.add(lesson)
    session.commit()

def add_teacher_lesson(lesson_teacher):
    session.add(lesson_teacher)
    session.commit()

def update_lessons_teacher(current_lesson, teacher_id):
    query = update(Lesson).where(Lesson.id == current_lesson.id).values(teacher_id=teacher_id)
    query2 = update(TeacherLesson).where(TeacherLesson.lesson_id == current_lesson.id).values(teacher_id=teacher_id)
    session.execute(query)
    session.execute(query2)
    session.commit()

def get_student_all_lesson(student_id):
    lessons = session.query(StudentLesson).filter(StudentLesson.student_id == student_id).all()
    return lessons

def get_current_semester(student_id, year, semester):
    return session.query(StudentLesson).filter((StudentLesson.student_id == student_id) & (StudentLesson.years == year) & (StudentLesson.semester_type == semester)).all()

def get_options(student_id):
    query = select(distinct(StudentLesson.years)).where(StudentLesson.student_id == student_id)
    result_year = session.execute(query)
    query = select(distinct(StudentLesson.semester_type)).where(StudentLesson.student_id == student_id)
    result_semester = session.execute(query)

    years = [row[0] for row in result_year]
    semesters = [row[0] for row in result_semester]

    return years, semesters
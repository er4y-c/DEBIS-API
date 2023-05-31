from db.database import Session, engine
from models.models import Lesson, Teacher, Student, StudentLesson, TeacherLesson

session = Session(bind=engine)

def get_lesson_by_code(lesson_code):
    return session.query(Lesson).filter(lesson_code == Lesson.lesson_code).first()

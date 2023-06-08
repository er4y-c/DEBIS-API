from db.database import Session, engine
from models.models import Lesson, Teacher, Student, StudentLesson, TeacherLesson

session = Session(bind=engine)

def get_student_by_no(student_no):
    return session.query(Student).filter(student_no == Student.student_no).first()

def get_teacher_by_id(teacher_id):
    return session.query(Teacher).filter(Teacher.id == teacher_id).first()

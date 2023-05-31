from crud.user import get_student_by_no
from db.database import Session, engine
from models.models import StudentLesson

session = Session(bind=engine)

def create_id_list(student_list):
    student_id_list = []

    for student_no in student_list:
        student = get_student_by_no(student_no)
        student_id_list.append(student.id)

    return student_id_list

def assign_lesson(student_id_list, lesson_id):

    for i in student_id_list:
        new_student_lesson = StudentLesson(
            lesson_id = lesson_id,
            student_id = i,
            ara_sinav = None,
            final = None,
            diger_sinav = None,
        )
        session.add(new_student_lesson)
        session.commit()    
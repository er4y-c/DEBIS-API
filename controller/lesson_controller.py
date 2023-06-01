from crud.user import get_student_by_no
from crud.lesson import get_lesson_by_code, update_notes
from db.database import Session, engine
from models.models import StudentLesson, Lesson

session = Session(bind=engine)

def create_id_list(student_list):
    student_id_list = []

    for student_no in student_list:
        student = get_student_by_no(student_no)
        student_id_list.append(student.id)

    return student_id_list

def assign_lesson_controller(student_id_list, lesson_id):

    for i in student_id_list:
        new_student_lesson = StudentLesson(
            lesson_id = lesson_id,
            student_id = i,
            ara_sinav = None,
            final = None,
            diger_sinav = None,
        )
        return new_student_lesson

def add_notes_controller(note_data):
    current_lesson = get_lesson_by_code(note_data.lesson_code)
    for i in range(len(note_data.student_no)):
        current_student = get_student_by_no(note_data.student_no[i])
        update_notes(
            student_id = current_student.id,
            lesson_id = current_lesson.id,
            ara_sinav = note_data.ara_sinav[i],
            final = note_data.final[i],
            diger_sinav = note_data.diger_sinav[i],
        )
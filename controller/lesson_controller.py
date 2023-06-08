from crud.user import get_student_by_no, get_teacher_by_id
from crud.lesson import get_lesson_by_code, update_notes, update_lessons_teacher, get_lesson_by_id
from db.database import Session, engine
from models.models import StudentLesson, TeacherLesson, Lesson

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

def assign_teacher_controller(lesson_code, teacher_id):
    try:
        current_lesson = get_lesson_by_code(lesson_code)
        update_lessons_teacher(current_lesson, teacher_id)

        return True
    except Exception as e:
        return None

def lesson_data_controller(lesson_id):
    lesson_data = get_lesson_by_id(lesson_id)
    teacher_data = get_teacher_by_id(lesson_data.teacher_id)

    return {
    "id": lesson_data.id,
    "teacher": teacher_data.full_name,
    "lesson_department": lesson_data.lesson_department,
    "lesson_name": lesson_data.lesson_name,
    "lesson_code": lesson_data.lesson_code,
    "lesson_credit": lesson_data.lesson_credit
  }

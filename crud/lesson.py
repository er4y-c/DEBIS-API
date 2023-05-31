from db.database import Session, engine
from models.models import Lesson, StudentLesson
from sqlalchemy import update

session = Session(bind=engine)

def get_lesson_by_code(lesson_code):
    return session.query(Lesson).filter(lesson_code == Lesson.lesson_code).first()

def update_notes(student_id, lesson_id, ara_sinav, final, diger_sinav):
    
    temp = update(StudentLesson).where(StudentLesson.student_id == student_id and StudentLesson.lesson_id == lesson_id).values(ara_sinav=ara_sinav, final=final, diger_sinav=diger_sinav)
    session.execute(temp)
    session.commit()
from db.database import Session, engine
from models.models import Announcement, Lesson

session = Session(bind=engine)

def get_all_announcement():
    return session.query(Announcement).all()

def add_announcement(new):
    session.add(new)
    session.commit()

def get_announcement_by_lesson(lesson_id):
    return session.query(Announcement).filter(Announcement.lesson_id == lesson_id).all()

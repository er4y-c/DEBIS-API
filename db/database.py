from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dynaconf import settings
from models.models import Student, Teacher, Lesson, StudentLesson, TeacherLesson, Announcement

engine = create_engine(settings.POSTGRE_SQL_URL, echo=True)
Session = sessionmaker(bind=engine)
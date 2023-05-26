from db.database import Base
from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String(80), unique=True, index=True)
    password = Column(Text)
    student_no = Column(String(10))
    student_department = Column(String(80))
    student_major = Column(String(80))
    semester = Column(Integer)
    is_active = Column(Boolean, default=False)
    enrollment_date = Column(DateTime)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(80), unique=True, index=True)
    password = Column(Text)
    teacher_department = Column(String(80))
    teacher_major = Column(String(80))

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    lesson_code = Column(String(10), unique=True)
    lesson_name = Column(String(50))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    lesson_credit = Column(Integer)
    lesson_department = Column(String(80))
    teacher = relationship("Teacher", back_populates="lessons")

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    announcement_title = Column(Text)
    announcement_content = Column(Text)
    announcement_date = Column(DateTime)
    lesson = relationship("Lesson", back_populates="announcements")

class StudentLesson(Base):
    __tablename__ = "student_lessons"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))

class TeacherLesson(Base):
    __tablename__ = "teacher_lessons"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
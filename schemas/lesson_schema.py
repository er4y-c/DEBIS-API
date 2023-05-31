from pydantic import BaseModel
from typing import Optional

class AddLessonModel(BaseModel):
    id: Optional[int]
    lesson_code: str
    lesson_name: str
    teacher_id: Optional[int]
    lesson_credit: int
    lesson_department: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
               "lesson_code": "CS-101",
               "lesson_name": "Introduction Computer Science-1",
               "lesson_credit": 6,
               "lesson_department": "Computer Science"
            }
        }

class AddStudentLessonModel(BaseModel):
    id: Optional[int]
    lesson_code: str
    student_list: list[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
               "lesson_code": "CS-101",
               "student_list": ["2020280128", "2020280129"], 
            }
        }

class AddNoteModel(BaseModel):
    student_no: list[str]
    lesson_code: str
    ara_sinav: list[int]
    final: list[int]
    diger_sinav: list[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
               "student_no": ["2020280128", "2020280129"],
               "lesson_code": "CS-101",
               "ara_sinav": [100, 0],
               "final": [0, 50],
               "diger_sinav": [0, 100],
            }
        }
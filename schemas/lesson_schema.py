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
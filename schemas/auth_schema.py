from pydantic import BaseModel
from typing import Optional
from datetime import date

class LoginModel(BaseModel):
    email: str
    password: str
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "erayaynaci@school.edu.tr",
                "password": "123456",
            }
        }

class SignUpStudentModel(BaseModel):
    id: Optional[int] 
    email: str
    password: str
    is_active: Optional[bool] = False
    first_name: str
    last_name: str
    student_no: str
    student_department: Optional[str]
    student_major: Optional[str]
    semester: Optional[int]
    enrollment_date: Optional[date]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "erayaynaci@school.edu.tr",
                "password": "123456",
                "first_name": "Eray",
                "last_name": "Aynacı",
                "student_no": "2020280128"
            }
        }

class SignUpTeacherModel(BaseModel):
    id: Optional[int] 
    email: str
    password: str
    first_name: str
    last_name: str
    teacher_department: Optional[str]
    teacher_major: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "elifmertturk@school.edu.tr",
                "password": "123456",
                "first_name": "Elif",
                "last_name": "Merttürk",
                "teacher_department": "Fen Fakültesi",
                "teacher_major": "Bilgisayar Bilimleri",
            }
        }
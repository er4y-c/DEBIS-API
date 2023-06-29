from pydantic import BaseModel
from typing import Optional

class AnnouncementModel(BaseModel):
    id: Optional[int]
    lesson_code: str
    title: str
    content: str

    class Config:
        orm_mode: True
        schema_extra = {
            "example": {
               "lesson_code": "CS-101",
               "title": "Deneme",
               "content": "Deneme",
            }
        }
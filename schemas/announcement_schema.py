from pydantic import BaseModel
from typing import Optional

class AnnouncementModel(BaseModel):

    class Config:
        orm_mode: True
        schema_extra = {
            "example": {
               "lesson_code": "CS-101",
               "title": "Deneme",
               "content": "Deneme",
               "date": "29-06-2023"
            }
        }
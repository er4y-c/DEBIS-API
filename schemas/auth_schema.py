from pydantic import BaseModel

class LoginModel(BaseModel):
    email: str
    password: str
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "johndoe@school.edu.tr",
                "password": "123456",
            }
        }
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from controller.auth_controller import authenticate_user, create_access_token, get_current_user
from models.models import Student
from schemas.auth_schema import SignUpStudentModel, LoginModel
from db.database import Session, engine

router = APIRouter()
session = Session(bind=engine)

@router.get("/")
async def hello(token: str = Depends(get_current_user)):
    return {"message":"hello world"}

@router.post("/login")
async def login(user: LoginModel):
    auth_user = authenticate_user(user)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Geçersiz kullanıcı adı veya şifre")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/save_student")
async def save_student(user: SignUpStudentModel):
    existing_user = authenticate_user(user)
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı zaten mevcut")
    
    new_user=Student(
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        student_no=user.student_no
    )
    
    session.add(new_user)
    session.commit()
    return JSONResponse(
        status_code=200,
        content= {"message": "Kullanıcı başarıyla kaydedildi"}
    )
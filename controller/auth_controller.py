from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dynaconf import settings
from schemas.auth_schema import LoginModel
from db.database import Session, engine
from models.models import Student, Teacher
from fastapi.security import OAuth2PasswordBearer
from fastapi import Security, HTTPException
from models.models import Student

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
session = Session(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(user: LoginModel):
    db_user = session.query(Student).filter(Student.email == user.email).first()
    if not db_user:
        db_user = session.query(Teacher).filter(Teacher.email == user.email).first()

    return user if verify_password(user.password, get_password_hash(user.password)) and db_user else None

def authenticate_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email:
            db_user = session.query(Student).filter(Student.email == email).first()
            if not db_user:
                db_user = session.query(Teacher).filter(Teacher.email == email).first()
            return db_user
    except (JWTError, AttributeError):
        return None

    return None

def get_current_user(token: str = Security(oauth2_scheme)):
    user = authenticate_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
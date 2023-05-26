from fastapi import FastAPI
from routes.auth_routes import router as auth_routes

app = FastAPI()

app.include_router(router=auth_routes, prefix="/auth", tags=["auth"])
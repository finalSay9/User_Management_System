from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List,Optional
import src.Users.users as users
import src.Authentication.auth as auth
from src.DB import models
from src.DB.database import engine
import src.Departments.department as department




models.Base.metadata.create_all(bind=engine)
app = FastAPI(title= 'Company Management System')

app.include_router(users.router, tags=['create_users'])
app.include_router(auth.router, tags=['auth'])
app.include_router(department.router, tags='department')





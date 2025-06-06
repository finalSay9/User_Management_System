from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List,Optional
import users
import auth


app = FastAPI(title= 'User Blog')

app.include_router(users.router, tags=['create_users'])
app.include_router(auth.router, tags=['auth'])





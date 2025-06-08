from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List,Optional
import src.Users.users as users
import src.Authentication.auth as auth


app = FastAPI(title= 'User Blog')

app.include_router(users.router, tags=['create_users'])
app.include_router(auth.router, tags=['auth'])





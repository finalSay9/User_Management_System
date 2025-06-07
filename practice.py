from fastapi import Security, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Optional
from datetime import timedelta, datetime
from jose import jwt

#handling authentication and authorization


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Store securely
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')

#creating an instance used to to hash passwords
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

#lest hash passwords here 
def hash_pwd(password: str) -> str:
    hashed_pwd = pwd_context.hash(password)
    return hashed_pwd

#helper function for creating jwt
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    #copying the input data
    to_encode = data.copy()
    #seeting caculating expire time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow + timedelta(minutes=15)
    
    to_encode = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



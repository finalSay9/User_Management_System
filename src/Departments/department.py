from fastapi import APIRouter, Depends
from src.DB import schema, models
from typing import List
from sqlalchemy.orm import Session


router = APIRouter()

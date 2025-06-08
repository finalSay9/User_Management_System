from fastapi import APIRouter, Depends
from Authentication import auth
from src.DB import schema, models, database
from typing import List
from sqlalchemy.orm import Session


router = APIRouter()

#department endpoint
@router.post('/deparments',response_model=schema.DepartmentCreate)
def create_deparment(
    deparment: schema.DepartmentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.Create_User = Depends(auth.chec)
    )

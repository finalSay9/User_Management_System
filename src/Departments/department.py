from fastapi import APIRouter, Depends, HTTPException
from src.Authentication import auth
from src.DB import schema, models, database
from typing import List
from sqlalchemy.orm import Session
from src.Authentication import crud


router = APIRouter()

#department endpoint
@router.post('/deparments',response_model=schema.DepartmentCreate)
def create_deparment(
    deparment: schema.DepartmentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.Create_User = Depends(auth.check_admin_hr_access)
    ):
    return crud.create_department(db=db, department=deparment)


@router.get("/departments/", response_model=List[schema.Department])
def read_departments(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db), 
    current_user: schema.UserCreate = Depends(auth.get_current_active_user)
):
    departments = crud.get_departments(db, skip=skip, limit=limit)
    return departments


@router.get("/departments/{department_id}", response_model=schema.Department)
def read_department(
    department_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: schema.UserCreate = Depends(auth.get_current_active_user)
):
    db_department = crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department


@router.put("/departments/{department_id}", response_model=schema.Department)
def update_department(
    department_id: int, 
    department_data: schema.DepartmentBase, 
    db: Session = Depends(database.get_db), 
    current_user: schema.UserCreate = Depends(auth.check_admin_hr_access)
):
    return crud.update_department(db, department_id, department_data)


@router.delete("/departments/{department_id}")
def delete_department(
    department_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: schema.UserCreate = Depends(auth.check_admin_access)
):
    return crud.delete_department(db, department_id)

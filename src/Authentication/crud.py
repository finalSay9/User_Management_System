
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.DB import schema, models
from src.Authentication.auth import get_password_hash


# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.Create_User).filter(models.Create_User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Create_User).filter(models.Create_User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Create_User).offset(skip).limit(limit).all()




def update_user(db: Session, user_id: int, user_data):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


# Department CRUD operations
def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.id == department_id).first()


def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()


def create_department(db: Session, department: schema.DepartmentCreate):
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def update_department(db: Session, department_id: int, department_data):
    db_department = get_department(db, department_id)
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for key, value in department_data.dict(exclude_unset=True).items():
        setattr(db_department, key, value)
    
    db.commit()
    db.refresh(db_department)
    return db_department


def delete_department(db: Session, department_id: int):
    db_department = get_department(db, department_id)
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(db_department)
    db.commit()
    return {"message": "Department deleted successfully"}


# Employee CRUD operations
def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: schema.EmployeeCreate):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, employee_data):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in employee_data.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}


# Leave Request CRUD operations
def get_leave_request(db: Session, leave_id: int):
    return db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()


def get_leave_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LeaveRequest).offset(skip).limit(limit).all()


def get_employee_leave_requests(db: Session, employee_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.LeaveRequest).filter(
        models.LeaveRequest.employee_id == employee_id
    ).offset(skip).limit(limit).all()


def create_leave_request(db: Session, leave_request: schema.LeaveRequestCreate):
    db_leave = models.LeaveRequest(**leave_request.dict())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave


def update_leave_request(db: Session, leave_id: int, leave_data, approver_id: Optional[int] = None):
    db_leave = get_leave_request(db, leave_id)
    if not db_leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    for key, value in leave_data.dict(exclude_unset=True).items():
        setattr(db_leave, key, value)
    
    if approver_id:
        db_leave.approver_id = approver_id
    
    db.commit()
    db.refresh(db_leave)
    return db_leave


def delete_leave_request(db: Session, leave_id: int):
    db_leave = get_leave_request(db, leave_id)
    if not db_leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    db.delete(db_leave)
    db.commit()
    return {"message": "Leave request deleted successfully"}

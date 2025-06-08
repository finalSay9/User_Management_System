from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    EMPLOYEE = "employee"
    HR = "hr"
    MANAGER = "manager"



class UserCreate(BaseModel): # user in 
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    password: str
    role: UserRole = UserRole.EMPLOYEE

class UserRoleUpdate(BaseModel):
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DepartmentCreate(BaseModel):
    pass

class Department(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] =None

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    user_id: int
    department_id: int
    postion: set
    hire_date: datetime
    salary: float

class Employee(EmployeeBase):
    id: int
    create_at: datetime
    update_at: Optional[datetime] = None
    user: UserCreate
    department: Department

    class Config:
        from_attribute = True






class UserOut(UserCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

        

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserDeleter(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
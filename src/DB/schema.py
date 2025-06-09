from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Optional
from enum import Enum



class UserRole(str, Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    EMPLOYEE = "employee"
    HR = "hr"
    MANAGER = "manager"

class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LeaveType(str, Enum):
    SICK = "sick"
    VACATION = "vacation"
    PERSONAL = "personal"
    OTHER = "other"

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    dob: date
    gender: str
    password: str
    role: UserRole = UserRole.EMPLOYEE
    department_ids: List[int] = []

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserRoleUpdate(BaseModel):
    role: UserRole

class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    dob: date
    gender: str
    role: UserRole
    department_ids: List[int]
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    manager_id: Optional[int] = None
    user_ids: List[int] = []

class Department(DepartmentBase):
    id: int
    manager_id: Optional[int]
    user_ids: List[int]
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    user_id: int
    department_id: int
    position: str  # Fixed typo
    hire_date: datetime
    salary: float

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class LeaveRequestBase(BaseModel):
    employee_id: int
    start_date: datetime
    end_date: datetime
    leave_type: LeaveType
    reason: Optional[str] = None

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequest(LeaveRequestBase):
    id: int
    status: LeaveStatus = LeaveStatus.PENDING
    approver_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class UserDeleter(BaseModel):  # Consider removing if unused
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
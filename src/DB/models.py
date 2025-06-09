from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Table, Text, func
from src.DB.database import Base
from sqlalchemy.orm import relationship
from src.DB.schema import UserRole 
from src.DB.schema import LeaveRequest,LeaveType,LeaveStatus




# Junction table for many-to-many relationship
user_department = Table(
    'user_department',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('department_id', Integer, ForeignKey('departments.id'), primary_key=True)
)

#model for user 

class Create_User(Base):
    __tablename__='users'

    
    id = Column(Integer,primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True, nullable=False)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    phone_number = Column(String, index=True, nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    employee_info = relationship("Employee", uselist=False, back_populates="user")
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    reset_token =Column(String, nullable=True)
    reset_token_expire=Column(String, nullable=True)
    departments = relationship("Department", secondary=user_department, back_populates="users")
    


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    employees = relationship('Employee', back_populates="department")
    users = relationship("Create_User", secondary=user_department, back_populates="departments")



class Employee(Base):
    __tablename__ = "employees"


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    position = Column(String, nullable=False)
    hire_date = Column(DateTime, nullable=False)
    salary = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    user = relationship("Create_User", back_populates="employee_info")
    department = relationship("Department", back_populates="employees")
    leave_requests = relationship("LeaveRequest", back_populates="employee")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    leave_type = Column(Enum(LeaveType), nullable=False)
    reason = Column(String, nullable=True)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING, nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    employee = relationship("Employee", back_populates="leave_requests")
    approver = relationship("Create_User")



    
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from src.DB.database import Base
from sqlalchemy.orm import relationship
from src.DB.schema import UserRole 

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
    employee = relationship
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    reset_token =Column(String, nullable=True)
    reset_token_expire=Column(String, nullable=True)


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    employees = relationship('Employee', back_populates="departments")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    position = Column(String)
    hire_date = Column(DateTime)
    salary = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="employee")
    department = relationship("Department", back_populates="employees")



    
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text
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



    
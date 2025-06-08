from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from src.DB.database import Base


#model for user 

class Create_User(Base):
    __tablename__='users'

    
    id = Column(Integer,primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True, nullable=False)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    phone_number = Column(String, index=True, nullable=False)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)


    
from fastapi import APIRouter,Depends, HTTPException,status
import database
import models
from sqlalchemy.orm import Session
import schema
from typing import List
from auth import pwd_context, get_current_user



router = APIRouter()

#create user
@router.post('/user', response_model=schema.UserOut)
def user_create(
    user: schema.UserCreate,
    db: Session = Depends(database.get_db),
    ):
    existing_email = db.query(models.Create_User).filter(models.Create_User.email== user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail='the user with that email already exist')
    hashed_password = pwd_context.hash(user.password)
    user_db = models.Create_User (
        email= user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        password=hashed_password,
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


#gettings user
@router.get('/users', response_model=List[schema.UserOut])
def get_users(
    
    db: Session = Depends(database.get_db)
    ):
    getting_users = db.query(models.Create_User).all()
    return getting_users


#update the user
@router.put('/update_user', response_model=schema.UserOut)
def update_user(
    user_id: int,
    user: schema.UserUpdate,
    db: Session = Depends(database.get_db)
    ):

    #FIND USER IF EXIST
    updated_user = db.query(models.Create_User).filter(models.Create_User.id == user_id).first()
    if not updated_user:
        raise HTTPException(status_code=400, detail='User not found')
    
    #CHECK EMAIL UNIQUENESS IF EMAIL UPDATED 
    if user.email and user.email != updated_user.email:
        existing_email = db.query(models.Create_User).filter(models.Create_User.email == user.email).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user with that email already exist')
    
    #UPDATE FIELDS
    update_field = user.dict(exclude_unset=True)
    for key, value in update_field.items():
        setattr(updated_user,key, value)

    try:
        db.commit()
        db.refresh(updated_user)
        return updated_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=  f'Database error: {str(e)}')
        


#now lets delete the user 
@router.delete('/users/{user_id}', response_model=schema.UserOut)
def delete_user(
    user_id: int,
    user_deleted: schema.UserDeleter,
    db: Session = Depends(database.get_db),
 ):
    #check if the user existing using id
    existing_user = db.query(models.Create_User).filter(models.Create_User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='the user does not exist')
    
    #store user data to return b4 deletion
    try:

        user_data = existing_user
        db.delete(existing_user)
        db.commit()
        return user_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Database error: {str(e)}')
    
    

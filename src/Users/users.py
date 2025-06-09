from fastapi import APIRouter,Depends, HTTPException,status
import src.DB.database as database
import src.DB.models as models
from sqlalchemy.orm import Session
import src.DB.schema as schema
from typing import List
from src.Authentication.auth import pwd_context, get_current_user



router = APIRouter()

@router.post('/user', response_model=schema.UserOut)
def user_create(
    user: schema.UserCreate,
    db: Session = Depends(database.get_db),
):
    existing_email = db.query(models.Create_User).filter(models.Create_User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail='The user with that email already exists')

    hashed_password = pwd_context.hash(user.password)
    user_db = models.Create_User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        dob=user.dob,
        gender=user.gender,
        role=user.role,
        password=hashed_password,
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    # Associate departments if provided
    if user.department_ids:
        departments = db.query(models.Department).filter(models.Department.id.in_(user.department_ids)).all()
        if len(departments) != len(user.department_ids):
            raise HTTPException(status_code=400, detail="One or more department IDs are invalid")
        user_db.departments = departments
        db.commit()

    # Construct response with department_ids
    response_data = {
        "id": user_db.id,
        "email": user_db.email,
        "first_name": user_db.first_name,
        "last_name": user_db.last_name,
        "phone_number": user_db.phone_number,
        "dob": user_db.dob,
        "gender": user_db.gender,
        "role": user_db.role,
        "department_ids": [dept.id for dept in user_db.departments],
        "created_at": user_db.created_at,
        "updated_at": user_db.updated_at,
    }
    return response_data




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
    
    

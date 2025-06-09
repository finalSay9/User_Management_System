from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
from src.DB import models, schema, database
from src.Authentication import auth

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/superuser', response_model=schema.UserOut)
def create_superuser(
    superuser: schema.SuperUserCreate,
    db: Session = Depends(database.get_db)
):
    # Check if a superuser already exists
    existing_superuser = db.query(models.Create_User).filter(models.Create_User.role == schema.UserRole.SUPERUSER).first()
    if existing_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A superuser already exists"
        )

    # Check for existing email
    existing_email = db.query(models.Create_User).filter(models.Create_User.email == superuser.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email is already registered"
        )

    # Hash password
    hashed_password = pwd_context.hash(superuser.password)

    # Create superuser
    user_db = models.Create_User(
        email=superuser.email,
        password=hashed_password,
        role=schema.UserRole.SUPERUSER,
        created_at=datetime.utcnow()
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    # Construct response
    response_data = {
        "id": user_db.id,
        "email": user_db.email,
        "first_name": None,
        "last_name": None,
        "phone_number": None,
        "dob": None,
        "gender": None,
        "role": user_db.role,
        "department_ids": [],
        "created_at": user_db.created_at,
        "updated_at": user_db.updated_at,
    }
    return response_data

@router.post('/user', response_model=schema.UserOut)
def create_user(
    user: schema.UserCreate,
    db: Session = Depends(database.get_db),
    current_user: models.Create_User = Depends(auth.get_current_user)
):
    # Restrict user creation based on roles
    if current_user.role == schema.UserRole.SUPERUSER:
        if user.role not in [schema.UserRole.ADMIN, schema.UserRole.HR, schema.UserRole.MANAGER, schema.UserRole.EMPLOYEE]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Superuser can only create admins, HR, managers, or employees"
            )
    elif current_user.role == schema.UserRole.ADMIN:
        if user.role not in [schema.UserRole.ADMIN, schema.UserRole.HR, schema.UserRole.MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins can only create other admins, HR, or managers"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superuser or admins can create users"
        )

    # Check for existing email
    existing_email = db.query(models.User).filter(models.Create_User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email is already registered"
        )

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Create user
    user_db = models.User(
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more department IDs are invalid"
            )
        user_db.departments = departments
        db.commit()

    # Create Employee record if department_ids are provided
    if user.department_ids:
        for dept_id in user.department_ids:
            employee = models.Employee(
                user_id=user_db.id,
                department_id=dept_id,
                position="Default Position",  # Adjust as needed
                hire_date=datetime.utcnow(),
                salary=0.0,  # Adjust as needed
            )
            db.add(employee)
        db.commit()

    # Construct response
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
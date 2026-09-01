from os import access
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends,Request
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from schema import User
import models
from core import security
from typing import Annotated
from utilis.dependencies import rate_limiter


router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/register",dependencies=[Depends(rate_limiter)])
async def register_user(user:User,db:Session=Depends(get_db)):
    email_check = db.query(models.User).filter(models.User.email == user.email).first()

    if email_check :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already exists")
    
    encrypt_password = security.get_password_hash(user.password)

    new_user = models.User(
        email = user.email,
        password = encrypt_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"user created successfully"}

@router.post("/login",dependencies=[Depends(rate_limiter)])
def login(data:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not found")
    hashed_password = user.password
    if not security.verify_password(data.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect password")
    
    access = security.create_access_token(data={"sub":user.email,"id":user.id})

    return { "access_token": access, "token_type": "bearer" }
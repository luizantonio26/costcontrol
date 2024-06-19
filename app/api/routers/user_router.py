from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.models.user import LoginUserRequest, RegisterUserRequest, RegisterUserResponse, UpdateUserRequest, User
from app.configs.security import Token, authenticate_user, generate_tokens, get_current_user
from app.utils import hash_password, verify_password
from app.configs.dependencies import get_db


router = APIRouter()

@router.post("/token/", response_model=Token)
async def user_login(user_request: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(user_request.username, user_request.password, db)
    if user and verify_password(user_request.password, user.password):
        token = generate_tokens(user.email)
        return token
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/signin/", response_model=RegisterUserResponse)
async def register_user(user_request: RegisterUserRequest, db: Session = Depends(get_db)) -> RegisterUserResponse:
    if db.query(User).filter(User.email == user_request.email).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    if user_request.password != user_request.confirm_password:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="The password doesn't match")
        
    hashed_password = hash_password(user_request.password)
    
    del user_request.confirm_password
    
    user: User = User(**user_request.model_dump())
    user.password = hashed_password
    
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user # type: ignore

@router.get("/profile/", response_model=RegisterUserResponse)
async def get_user_profile(user: Annotated[User, Depends(get_current_user)]) -> RegisterUserResponse:
    return user # type: ignore
    
@router.patch("/profile/", response_model=RegisterUserResponse)
async def update_user_profile(user_request: UpdateUserRequest, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if user_request.birthdate == None and user_request.name == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The request has any field to update")
    
    if user_request.birthdate:
        user.birthdate = user_request.birthdate
    
    if user_request.name:
        user.name = user_request.name
    
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
    
    

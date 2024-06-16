from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.models.user import LoginUserRequest, RegisterUserRequest, RegisterUserResponse, User
from app.utils import hash_password, verify_password
from app.configs.dependencies import get_db


router = APIRouter()

@router.post("/login/", response_model=LoginUserRequest)
def user_login(user_request: LoginUserRequest, db: Session = Depends(get_db)) -> LoginUserRequest:
    user = db.query(User).filter(User.email == user_request.email).first()
    
    if user and verify_password(user_request.password, hashed_password=user.password):
        print("user authenticated")
        return user_request
    raise HTTPException(status_code=400, detail="Email or password invalid")

@router.post("/signin/", response_model=RegisterUserResponse)
def register_user(user_request: RegisterUserRequest, db: Session = Depends(get_db)) -> RegisterUserResponse:
    if db.query(User).filter(User.email == user_request.email).first():
        raise HTTPException(400, detail="Email already exists")
    
    if user_request.password != user_request.confirm_password:
        raise HTTPException(400, detail="The password doesn't match")
        
    hashed_password = hash_password(user_request.password)
    
    del user_request.confirm_password
    
    user = User(**user_request.model_dump())
    user.password = hashed_password
    
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user # type: ignore
    
    

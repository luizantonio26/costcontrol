from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

import jwt

from app.api.models.user import User
from app.configs.dependencies import get_db
from app.utils import verify_password


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    refresh_token: str

def generate_tokens(email: str) -> Token:
    access_payload = {
        "sub": email,
        "iat": datetime.now(timezone.utc), # type: ignore
        "exp": datetime.now(timezone.utc) + timedelta(days=1),  # Access token expira em 15 minutos # type: ignore
        "scope": "read write"
    }
    
    access_token = jwt.encode(payload=access_payload, key=SECRET_KEY, algorithm=ALGORITHM)
    
    
    refresh_payload = {
        "sub": email,
        "iat": datetime.now(timezone.utc), # type: ignore
        "exp": datetime.now(timezone.utc) + timedelta(days=15),  # refresh token expira em 15 minutos # type: ignore
    }
    
    refresh_token = jwt.encode(payload=refresh_payload, key=SECRET_KEY, algorithm=ALGORITHM)
    
    return Token(access_token=access_token, refresh_token=refresh_token)

def verify_token(token:str, token_type :str ="access"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if token_type == "access" and "scope" not in payload:
            raise jwt.InvalidTokenError("Invalid access token")
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidTokenError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(f"Invalid token: {e}")


def authenticate_user(email: str, password:str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    
    if user and verify_password(password, hashed_password=user.password):
        return user
    
    return False

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
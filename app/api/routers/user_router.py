import io
from typing import Annotated, Optional
from fastapi import Query, security
from typing_extensions import Doc
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBasic, HTTPBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pyotp import OTP
import pyotp
import qrcode
from sqlalchemy.orm import Session
from app.api.models.security_settings import SecuritySettings
from app.api.models.user import LoginUserRequest, RegisterUserRequest, RegisterUserResponse, UpdateUserRequest, User
from app.api.schemas.security_settings_schemas import SecuritySettingsSchema
from app.configs.security import Token, authenticate_user, generate_tokens, get_current_user
from app.utils import hash_password, verify_password
from app.configs.dependencies import get_db


router = APIRouter()
    
async def is_otp_correct(otp: Optional[str], secret: str) -> bool:
    return pyotp.TOTP(secret).now() == otp

@router.put("/otp/enable")
async def otp_enable(otp: bool, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    security_settings: SecuritySettings = db.query(SecuritySettings).get(user.security_settings) # type: ignore
    security_settings.otp_configured = not otp # type: ignore
    db.add(security_settings)
    db.commit()
    db.refresh(security_settings)

@router.get("/otp/generate")
def generate_qr_code(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    security_settings: SecuritySettings = db.query(SecuritySettings).get(user.security_settings) # type: ignore
    totp = pyotp.TOTP(security_settings.secret) # type: ignore
    qr_code = qrcode.make(
        totp.provisioning_uri(name=user.email, issuer_name="Controlcost")
    )
    img_byte_arr = io.BytesIO()
    qr_code.save(img_byte_arr)
    img_byte_arr = img_byte_arr.getvalue()
    return Response(content=img_byte_arr, media_type="image/png")


@router.post("/token/", response_model=Token)
async def user_login(
                    user_request: Annotated[OAuth2PasswordRequestForm, Depends()],
                    otp: Optional[str] = Query(None),
                    db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(user_request.username, user_request.password, db)
    if user and verify_password(user_request.password, user.password):
        if user.security_settings:
            security_settings: SecuritySettings = db.query(SecuritySettings).get(user.security_settings) # type: ignore
            if security_settings.otp_configured and not otp: # type: ignore
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2fa activated, you should send the opt code")
            if security_settings.otp_configured and not await is_otp_correct(otp, security_settings.secret): # type: ignore
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="otp code invalid")
                
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
    
    security_schema = SecuritySettingsSchema(otp_configured = False, secret=pyotp.random_base32())
    security_settings = SecuritySettings(**security_schema.model_dump())
    db.add(security_settings)
    db.commit()
    db.refresh(security_settings)
    
    user.security_settings = security_settings.id # type: ignore
    
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
    
    

import pyotp
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Boolean, Date, ForeignKey, Integer, Column, func
from sqlalchemy import String


class Base(DeclarativeBase):
    pass

class SecuritySettings(Base):
    __tablename__="security_settings"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    otp_configured = Column(Boolean, default=False)
    secret = Column(String(100), default=pyotp.random_base32())
from sqlalchemy import  create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import Settings

SQLALCHEMY_DATABASE_URL = Settings().DATABASE_URL # type: ignore

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
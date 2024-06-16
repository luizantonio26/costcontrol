from typing import Annotated, Union

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from app.api.main import api_router

app = FastAPI(
    title="Control Recipes Cost and Profits API",
    description="This is an API for control the recipes costs and estimate a profit for your commerce",
    contact={"email":"luiz.rozendo01@gmail.com"},
)

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
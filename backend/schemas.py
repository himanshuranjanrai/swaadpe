from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=64,   # bcrypt-safe
        description="Password must be 8-64 characters"
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TiffinStatusOut(BaseModel):
    date: date
    lunch: bool
    dinner: bool

    class Config:
        from_attributes = True


class TiffinStatusUpdate(BaseModel):
    date: date
    lunch: bool | None = None
    dinner: bool | None = None
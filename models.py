from datetime import datetime
import re

from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):#Receive data from the user.

    full_name: str
    email: EmailStr
    password: str


    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):

        value = value.strip()

        if len(value) < 3:
            raise ValueError(
                "Full name must be at least 3 characters long."
            )

        if len(value) > 50:
            raise ValueError(
                "Full name cannot exceed 50 characters."
            )

        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValueError(
                "Full name can contain only letters and spaces."
            )

        return value


    @field_validator("password")
    @classmethod
    def validate_password(cls, password):

        if len(password) < 8:
            raise ValueError(
                "Password must contain at least 8 characters."
            )

        if len(password) > 20:
            raise ValueError(
                "Password cannot exceed 20 characters."
            )

        if " " in password:
            raise ValueError(
                "Password cannot contain spaces."
            )

        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", password):
            raise ValueError(
                "Password must contain at least one number."
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", password):
            raise ValueError(
                "Password must contain at least one special character."
            )

        return password


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

class Config:
    from_attributes = True


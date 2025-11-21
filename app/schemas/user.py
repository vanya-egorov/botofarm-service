from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    login: EmailStr
    password: str
    project_id: UUID
    env: str = Field(..., pattern="^(prod|preprod|stage)$")
    domain: str = Field(..., pattern="^(canary|regular)$")


class UserCreate(UserBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "login": "testuser@gmail.com",
                "password": "qwerty",
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "env": "prod",
                "domain": "regular"
            }
        }
    }


class UserResponse(BaseModel):
    id: UUID
    created_at: datetime
    login: str
    project_id: UUID
    env: str
    domain: str
    locktime: datetime | None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2025-01-01T12:00:00",
                "login": "testuser@gmail.com",
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "env": "prod",
                "domain": "regular",
                "locktime": None
            }
        }
    }


class UserListResponse(BaseModel):
    users: list[UserResponse]


class LockRequest(BaseModel):
    user_id: UUID
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
    }


class LockResponse(BaseModel):
    message: str
    user_id: UUID
    locked_at: datetime


class UnlockResponse(BaseModel):
    message: str
    user_id: UUID


from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator


# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# --- Camera Schemas ---
class CameraBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    location: Optional[str] = None
    stream_url: str

    @validator("stream_url")
    def validate_url(cls, v):
        if not v.startswith(("rtsp://", "http://", "https://")):
            raise ValueError("URL must start with rtsp, http, or https")
        return v


class CameraCreate(CameraBase):
    owner_id: int


class CameraResponse(CameraBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# --- MongoDB Event Schemas ---
class DetectionEvent(BaseModel):
    camera_id: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    label: str
    confidence: float
    bounding_box: List[int]  # [x, y, w, h]

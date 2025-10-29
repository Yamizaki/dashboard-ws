from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ImageCreate(BaseModel):
    image_data: str  # Base64 string

class ImageResponse(BaseModel):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    time: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    time: str
    created_at: datetime
    
    class Config:
        from_attributes = True
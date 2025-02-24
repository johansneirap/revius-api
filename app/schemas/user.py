from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    auth0_id: str

class UserUpdate(UserBase):
    email: Optional[EmailStr]
    username: Optional[str]
    

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
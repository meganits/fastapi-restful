from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Todo schemas
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    completed: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
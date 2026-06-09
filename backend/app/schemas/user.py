from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name : str
    age : int
    gender: str
    address : str
    phone_number : str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    id : int
    name : str
    age : int
    gender: str
    address : str
    phone_number : str

    class Config:
        from_attributes = True

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    name: str = Field(..., max_length=20)
    username: str = Field(..., max_length=20)
    password: str
    department: Optional[str] = None
    position: Optional[str] = None
    role_id: Optional[str] = None
    expired_date: Optional[datetime] = None
    rank: Optional[int] = None
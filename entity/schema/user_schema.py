from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None

class UserOut(BaseSchema):
    id: int
    username: str
    email: str
    is_active: bool

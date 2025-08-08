from pydantic import BaseModel


class LoginResponse(BaseModel):
    username: str
    access_token:str
    refresh_token:str
from pydantic import BaseModel
from typing import Optional

class Register(BaseModel) :
    email : str
    username : str
    password : str
    major : str

class Login(BaseModel) :
    email : str
    password : str

class UserDto(BaseModel):
    id: int
    email: str
    username: str
    password: str
    description: str
    major: str

class UserResponse(BaseModel) :
    id : int
    username : str
    description : Optional[str]
    major : str

from pydantic import BaseModel
from typing import Optional
from domain.user.table import User

class Register(BaseModel) :
    email : str
    username : str
    password : str

class Login(BaseModel) :
    email : str
    password : str

class UserResponse(BaseModel) :
    id : int
    email: str
    username : str
    description: Optional[str] = None
    major: list[str]

def create_user_response(user: User):
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        description=user.description,
        major=user.major.split('|')
    )
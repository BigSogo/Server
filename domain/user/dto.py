from pydantic import BaseModel
from typing import Optional
from domain.user.table import User

class Register(BaseModel) :
    email : str
    username : str
    password : str
    major : list[str]

class Login(BaseModel) :
    email : str
    password : str

class UserResponse(BaseModel) :
    id : int
    profile_img: Optional[str] = None
    email: str
    username : str
    description: Optional[str] = None
    major: list[str]

class EmailSend(BaseModel):
    email: str

class EmailAuthentication(BaseModel):
    email: str
    code: str

def create_user_response(user: User):
    return UserResponse(
        id=user.id,
        profile_img=user.profile_img,
        email=user.email,
        username=user.username,
        description=user.description,
        major=user.major.split('|')
    )
    
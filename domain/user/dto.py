from pydantic import BaseModel
from typing import Optional
from domain.profile.dto import ProfileResponse, create_profile_response
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
    profile: ProfileResponse


def create_user_response(user: User):
    return UserResponse(
        id=user.id,
        profile_img=user.profile_img,
        email=user.email,
        username=user.username,
        description=user.description,
        major=user.major.split('|'),
        profile=create_profile_response(user.profile)
    )
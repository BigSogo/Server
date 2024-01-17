from pydantic import BaseModel

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
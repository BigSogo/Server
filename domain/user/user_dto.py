from pydantic import BaseModel

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

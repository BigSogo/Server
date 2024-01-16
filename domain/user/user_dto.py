from pydantic import BaseModel

class Register(BaseModel) :
    email : str
    username : str
    password : str
    major : str

class Login(BaseModel) :
    email : str
    password : str
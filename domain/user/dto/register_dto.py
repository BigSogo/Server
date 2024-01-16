from pydantic import BaseModel;

class Register(BaseModel) :
    email : str
    name : str
    username : str
    password : str
    major : str
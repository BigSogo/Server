from pydantic import BaseModel;

class Register(BaseModel) :
    username : str
    password : str
    major : str
    email : str
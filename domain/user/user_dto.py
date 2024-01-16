from pydantic import BaseModel;

class Register(BaseModel) :
    email : str
    username : str
    password : str
    major : str
from pydantic import BaseModel

class CreateQuestion(BaseModel):
    title: str
    content: str
    user_id: int
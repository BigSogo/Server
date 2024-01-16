from pydantic import BaseModel

class CreateQuestionRequest(BaseModel):
    title: str
    content: str
    userId: int
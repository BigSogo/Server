from pydantic import BaseModel
from datetime import datetime
from domain.user.dto import UserResponse

class CommentDto(BaseModel):
    id: int
    content: str
    date: datetime
    writer: UserResponse

class CreateComment(BaseModel):
    content: str
    question_id: int
    
class UpdateComment(BaseModel):
    comment_id: int
    content: str
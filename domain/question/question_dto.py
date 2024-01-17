from pydantic import BaseModel
from datetime import datetime
from domain.user.user_dto import UserDto
from domain.question.comment_dto import CommentDto

class CreateQuestion(BaseModel):
    title: str
    content: str
    user_id: int

class GetQuestion(BaseModel):
    id: int
    title: str
    content: str
    date: datetime
    writer: UserDto
    senior: UserDto
    comments: list[CommentDto]
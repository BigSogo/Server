from pydantic import BaseModel
from datetime import datetime
from domain.user.user_dto import UserResponse
from domain.question.comment_dto import CommentDto
from typing import Optional

class CreateQuestion(BaseModel):
    title: str
    content: str
    senior_id: Optional[int] = None

class GetQuestion(BaseModel):
    id: int = None
    title: str = None
    content: str = None
    date: datetime = None
    writer: UserResponse = None
    senior: Optional[UserResponse] = None
    comments: list[Optional[CommentDto]] = None
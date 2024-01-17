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
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    date: Optional[datetime] = None
    writer: Optional[UserResponse] = None
    senior: Optional[UserResponse] = None
    comments: list[Optional[CommentDto]] = None
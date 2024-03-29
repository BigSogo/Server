from pydantic import BaseModel
from datetime import datetime
from domain.user.dto import UserResponse
from domain.comment.dto import CommentDto
from typing import Optional

class CreateQuestion(BaseModel):
    title: str
    content: str
    senior_id: Optional[int] = None

class GetQuestion(BaseModel):
    id: int
    title: str
    content: str
    date: datetime
    writer: UserResponse
    senior: Optional[UserResponse] = None
    comments: list[Optional[CommentDto]] = None

class GetQuestionList(BaseModel):
    id: int
    title: str
    content: str
    date: datetime
    writer: UserResponse
    senior: Optional[UserResponse] = None
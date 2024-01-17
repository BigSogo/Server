from pydantic import BaseModel
from datetime import datetime
from domain.user.user_dto import UserDto

class CommentDto(BaseModel):
    id: int
    content: str
    date: datetime
    writer: UserDto
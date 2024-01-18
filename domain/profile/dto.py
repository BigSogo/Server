from pydantic import BaseModel
from domain.user.dto import UserResponse

class ProfileResponse(BaseModel):
    id: int
    user: UserResponse
    subject: str
    content: str
    portfolio_url: str
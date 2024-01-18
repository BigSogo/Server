from pydantic import BaseModel

from domain.profile.table import Profile
from domain.user.dto import UserResponse

class ProfileResponse(BaseModel):
    id: int
    subject: str
    content: str
    portfolio_url: str

class ProfileListResponse(BaseModel):
    user: UserResponse
    profiles: list[ProfileResponse]

def create_profile_response(profile: Profile) :
    return ProfileResponse(
        id=profile.id,
        subject=profile.subject,
        content=profile.content,
        portfolio_url=profile.portfolio_url
    )
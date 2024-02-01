# 기본 모듈
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 관련 모듈
from domain.user.table import User
from domain.profile.dto import ProfileListResponse, create_profile_response
from domain.user.dto import create_user_response

from globals.db import get_db
from globals.base_response import BaseResponse

router = APIRouter()

# 포트폴리오 가져오기
@router.get("/{user_id}", response_model=BaseResponse[ProfileListResponse])
async def get_profile(user_id: int, db: Session = Depends(get_db)) :
    user: User = db.query(User).get(user_id)

    profile_list = ProfileListResponse(
        user=create_user_response(user),
        profiles=[create_profile_response(profile) for profile in user.profile]
    )

    return BaseResponse(
        code = 200,
        message = "프로필 검색 성공",
        data = profile_list
    )
# 기본 모듈
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

# 관련 모듈
from globals.db import get_db
from domain.profile.table import Profile
from globals.base_response import BaseResponse
from domain.profile.dto import ProfileResponse
from domain.user.table import
from domain.user.dto import create_user_response

router = APIRouter()

# 포트폴리오 가져오기
@router.get("", response_model=BaseResponse)
async def get_profile(query: Optional[str] = None, db: Session = Depends(get_db)) :
    results = db.query(Profile).filter(Profile.major.like(f"%{query}%"))

    datas = [ProfileResponse(
        id=profile.id,
        user=create_user_response(profile.user),
        subject=profile.subject,
        content=profile.content,
        portfolio_url=profile.portfolio_url
    ) for profile in results]

    return BaseResponse(
        code = 200,
        message = "프로필 검색 성공",
        data = datas
    )
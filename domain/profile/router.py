# 기본 모듈
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 관련 모듈
from globals.db import get_db
from domain.profile.table import Profile
from globals.base_response import BaseResponse

router = APIRouter()

# 포트폴리오 가져오기
@router.get("/{id}", response_model=BaseResponse)
async def get_profile(id: int, db: Session = Depends(get_db)) :
    return BaseResponse(
        code = 200,
        message = "프로필 검색 성공",
        data = db.query(Profile).filter(Profile.id == id).first()
    )
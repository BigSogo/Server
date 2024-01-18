# 기본 모듈
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

# 관련 모듈
from globals.db import get_db
from domain.profile.table import Profile
from globals.base_response import BaseResponse
from domain.profile.dto import ProfileResponse
from domain.user.dto import create_user_response
from domain.user.table import User
from globals.jwt import get_current_user

router = APIRouter()

# 포트폴리오 가져오기
@router.get("", response_model=BaseResponse)
async def get_profile(query: Optional[str] = None, db: Session = Depends(get_db)) :
    results = db.query(User).filter(Profile.major.like(f"%{query}%"))

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

@router.patch("/update-image", response_model=BaseResponse)
async def update_image(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)) :
    image = await file.read()

    user = db.query(User).filter(User.id == current_user["id"]).first()

    if user :
        user.profile_img = image
        db.add(user)
        db.commit()
        return BaseResponse(
            code = 200,
            message = "이미지 업로드 성공",
            data = None
        )
    else :
        raise HTTPException(400, "잘못된 정보")

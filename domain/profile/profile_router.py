# 기본 모듈
from FastAPI import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

# 관련 모듈
from globals.db import get_db
from domain.profile.profile_table import Profile

router = APIRouter()

# 포트폴리오 가져오기
@router.get("")
async def get_profile(query: Optional[str] = None, db: Session = Depends(get_db)) :
    db.query(Profile).filter(Profile.major.like(f"%{query}%"))
    